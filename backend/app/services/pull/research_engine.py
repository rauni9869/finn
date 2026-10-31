from datetime import datetime, timezone
from typing import Dict, Any, Optional

from app.models.schemas import (
    DeliveryVerdict,
    FullResearchReport,
    FinancialSnapshotResponse,
    NarrativeMatrixResponse,
    NarrativeMatrixItem,
    BullBearThesisResponse,
    BusinessSnapshot,
    BalanceSheetHealth,
    CashQuality,
    ManagementGuidance,
    PrimaryDocuments,
    PrimaryDocumentItem
)
from app.services.data_fetchers.screener_scraper import screener_service

class PullResearchEngine:
    """Delivers institutional-grade research grounded 100% in primary filings & transcripts."""

    def get_company_deep_dive(self, ticker: str) -> FullResearchReport:
        clean_ticker = ticker.upper().replace(".NS", "").replace(".BO", "")
        raw_data = screener_service.get_company_fundamentals(clean_ticker)

        company_name = raw_data.get("company_name", f"{clean_ticker} Ltd")
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        # 1. Financial Snapshot (MVP)
        fin_raw = raw_data["financial_snapshot"]
        financial_snapshot = FinancialSnapshotResponse(**fin_raw)

        # 2. Narrative vs Numbers Matrix (Flagship MVP)
        narr_raw = raw_data["narrative_matrix"]
        narrative_items = [NarrativeMatrixItem(**item) for item in narr_raw.get("items", [])]
        delivered = sum(1 for i in narrative_items if i.verdict == DeliveryVerdict.DELIVERED)
        total = len(narrative_items)
        narrative_matrix = NarrativeMatrixResponse(
            ticker=clean_ticker,
            company_name=company_name,
            coverage_period=narr_raw.get("coverage_period", "Not assessed"),
            overall_track_record_score=f"{delivered} of {total} promises delivered" if total else "Not assessed",
            delivered_pct=round(delivered / total * 100) if total else None,
            summary_verdict=narr_raw.get("summary_verdict", "Not assessed."),
            items=narrative_items
        )

        # 3. Bull vs Bear Thesis (MVP)
        bb_raw = raw_data["bull_bear_thesis"]
        bull_bear_thesis = BullBearThesisResponse(**bb_raw)

        # 4. Business Snapshot (Stretch)
        biz_snapshot = None
        if "business_snapshot" in raw_data:
            biz_snapshot = BusinessSnapshot(**raw_data["business_snapshot"])

        # 5. Balance Sheet & Working Capital with RPTs and Auditor Check (Stretch)
        bal_sheet = None
        if "balance_sheet" in raw_data:
            bal_sheet = BalanceSheetHealth(**raw_data["balance_sheet"])

        # 6. Cash Quality & Conversion (Stretch)
        cash_qual = None
        if "cash_quality" in raw_data:
            cash_qual = CashQuality(**raw_data["cash_quality"])

        # 7. Management Guidance (Stretch)
        mgmt_guidance = None
        if "guidance" in raw_data:
            mgmt_guidance = ManagementGuidance(**raw_data["guidance"])

        # 8. Primary Document Links (Annual Reports & Concalls from screener.in)
        primary_docs = None
        if "primary_documents" in raw_data and raw_data["primary_documents"]:
            docs_raw = raw_data["primary_documents"]
            primary_docs = PrimaryDocuments(
                annual_reports=[PrimaryDocumentItem(**d) for d in docs_raw.get("annual_reports", [])],
                concall_transcripts=[PrimaryDocumentItem(**d) for d in docs_raw.get("concall_transcripts", [])]
            )

        return FullResearchReport(
            ticker=clean_ticker,
            company_name=company_name,
            timestamp=now_str,
            data_source=raw_data.get("data_source", "curated_sample"),
            financial_snapshot=financial_snapshot,
            narrative_matrix=narrative_matrix,
            bull_bear_thesis=bull_bear_thesis,
            primary_documents=primary_docs,
            business_snapshot=biz_snapshot,
            balance_sheet=bal_sheet,
            cash_quality=cash_qual,
            guidance=mgmt_guidance
        )

research_engine = PullResearchEngine()

