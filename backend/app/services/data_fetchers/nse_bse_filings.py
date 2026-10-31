import logging
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone, timedelta
import requests
from bs4 import BeautifulSoup

from app.models.schemas import (
    CorporateAnnouncement,
    AnnouncementCategory,
    PriorityLevel,
    ManagementBioEnrichment,
    QuarterlyResultsEnrichment,
    MetricDelta
)
from app.services.push.classifier import classifier
from app.services.data_fetchers.seed_data import SEED_ANNOUNCEMENTS

logger = logging.getLogger(__name__)

class CorporateFilingsService:
    """Ingests, classifies, and filters corporate filings from NSE/BSE with mock-first fallback."""

    def __init__(self):
        self._seed_announcements = SEED_ANNOUNCEMENTS

    def sample_data_as_of(self) -> datetime:
        return max(
            datetime.fromisoformat(item["timestamp"].replace("Z", "+00:00"))
            for item in self._seed_announcements
        )

    def get_announcements(
        self,
        ticker: Optional[str] = None,
        window_hours: int = 48,
        include_collapsed: bool = True
    ) -> List[CorporateAnnouncement]:
        """Retrieve prioritized corporate filings within the specified time window."""
        results: List[CorporateAnnouncement] = []
        now = datetime.now(timezone.utc)
        # Filings are a fixed sample, so the window is measured back from the newest one
        cutoff = self.sample_data_as_of() - timedelta(hours=window_hours)

        clean_target = ticker.upper().replace(".NS", "").replace(".BO", "") if ticker else None

        for item in self._seed_announcements:
            if clean_target and item["ticker"] != clean_target:
                continue

            # Parse timestamp
            try:
                ann_time = datetime.fromisoformat(item["timestamp"].replace("Z", "+00:00"))
            except Exception:
                ann_time = now

            if ann_time < cutoff:
                continue

            cat, prio, summary = classifier.classify(item["headline"], item["details"])
            
            # Use pre-annotated category/priority if present in seed, else classifier result
            category = item.get("category", cat)
            priority = item.get("priority", prio)
            one_line_summary = item.get("one_line_summary", summary)

            mgmt_enrich = None
            if "management_enrichment" in item and item["management_enrichment"]:
                m = item["management_enrichment"]
                mgmt_enrich = ManagementBioEnrichment(
                    incoming_person=m["incoming_person"],
                    new_role=m["new_role"],
                    effective_date=m["effective_date"],
                    predecessor=m.get("predecessor"),
                    career_profile_bullets=m.get("career_profile_bullets", []),
                    strategic_implication=m.get("strategic_implication", "")
                )

            res_enrich = None
            if "results_enrichment" in item and item["results_enrichment"]:
                r = item["results_enrichment"]
                res_enrich = QuarterlyResultsEnrichment(
                    quarter=r["quarter"],
                    revenue=MetricDelta(**r["revenue"]),
                    ebitda=MetricDelta(**r["ebitda"]),
                    pbt=MetricDelta(**r["pbt"]),
                    pat=MetricDelta(**r["pat"]),
                    headline_verdict=r["headline_verdict"],
                    key_highlights=r.get("key_highlights", [])
                )

            ann = CorporateAnnouncement(
                id=item["id"],
                ticker=item["ticker"],
                company_name=item["company_name"],
                timestamp=item["timestamp"],
                category=AnnouncementCategory(category) if isinstance(category, str) else category,
                priority=PriorityLevel(priority) if isinstance(priority, str) else priority,
                headline=item["headline"],
                details=item["details"],
                one_line_summary=one_line_summary,
                attachment_url=item.get("attachment_url"),
                management_enrichment=mgmt_enrich,
                results_enrichment=res_enrich
            )
            results.append(ann)

        # Sort: High Priority first, then Medium, then Low; secondary sort by timestamp desc
        priority_order = {PriorityLevel.HIGH: 0, PriorityLevel.MEDIUM: 1, PriorityLevel.LOW: 2}
        results.sort(key=lambda x: x.timestamp, reverse=True)
        results.sort(key=lambda x: priority_order.get(x.priority, 3))

        return results

    def fetch_live_nse_announcements(self) -> List[Dict[str, Any]]:
        """Optional live scraper for NSE India Corporate Announcements API."""
        url = "https://www.nseindia.com/api/corporate-announcements?index=equities"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.nseindia.com/companies-listing/corporate-filings-announcements"
        }
        session = requests.Session()
        try:
            # Bootstrap cookies from homepage
            session.get("https://www.nseindia.com", headers=headers, timeout=5)
            response = session.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.warning(f"Live NSE fetch failed: {e}. Utilizing resilient seed replay.")
        return []

filings_service = CorporateFilingsService()

