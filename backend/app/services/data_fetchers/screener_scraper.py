import copy
import logging
import re
import time
from typing import Dict, Any, Optional
from urllib.parse import quote, unquote
import requests
from bs4 import BeautifulSoup
from app.services.data_fetchers.seed_data import SEED_RESEARCH_PROFILES

logger = logging.getLogger(__name__)

# Common exchange ticker to Screener slug overrides (e.g. recent demergers/reclassifications)
SCREENER_TICKER_ALIASES = {
    "TATAMOTORS": "TMCV",
    "L&T": "LT",
    "MCDOWELL-N": "UNITDSPR"
}

class CompanyDataUnavailable(Exception):
    """No real data could be found for the requested ticker."""


class ScreenerScraperService:
    """Retrieves primary document links and standardized financials from screener.in."""

    def __init__(self, cache_ttl_seconds: int = 3600):
        self.cache_ttl = cache_ttl_seconds
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._seed_profiles = SEED_RESEARCH_PROFILES

    def get_company_fundamentals(self, ticker: str) -> Dict[str, Any]:
        """Fetch fundamentals for any NSE ticker. Raises CompanyDataUnavailable rather than inventing data."""
        clean_ticker = ticker.upper().replace(".NS", "").replace(".BO", "")
        live_data = None
        from app.core.config import settings
        if settings.ENABLE_LIVE_SCRAPING:
            try:
                live_data = self._get_live(clean_ticker)
            except Exception as e:
                logger.info(f"Live screener scrape for {clean_ticker} failed ({e}).")

        # A company name resolves to its ticker during the scrape
        seed = self._seed_profiles.get(clean_ticker)
        if not seed and live_data:
            seed = self._seed_profiles.get(live_data["ticker"])

        if seed:
            profile = copy.deepcopy(seed)
            profile["data_source"] = "curated_sample"
            if live_data:
                if live_data["primary_documents"]["annual_reports"] or live_data["primary_documents"]["concall_transcripts"]:
                    profile["primary_documents"] = live_data["primary_documents"]
                # An aliased ticker maps to a different listed entity, so its ratios don't apply here
                if clean_ticker not in SCREENER_TICKER_ALIASES:
                    for key in ("pe_ratio", "roce_pct", "roe_pct"):
                        if live_data["financial_snapshot"][key] is not None:
                            profile["financial_snapshot"][key] = live_data["financial_snapshot"][key]
            return profile

        if live_data:
            return live_data
        raise CompanyDataUnavailable(
            f"No data found for {clean_ticker}. Check the ticker or company name, or try again if the data source is unreachable."
        )

    def _get_live(self, ticker: str) -> Dict[str, Any]:
        entry = self._cache.get(ticker)
        if entry and time.time() - entry["cached_at"] < self.cache_ttl:
            return entry["data"]
        data = self._scrape_screener_live(ticker)
        self._cache[ticker] = {"cached_at": time.time(), "data": data}
        return data

    @staticmethod
    def _to_float(text: str) -> Optional[float]:
        try:
            return float(text.replace(",", "").replace("%", "").strip())
        except ValueError:
            return None

    def _latest_row_value(self, section, *labels: str) -> Optional[float]:
        """Latest column of the first table row whose label matches, ignoring the trailing '+'."""
        if not section:
            return None
        for row in section.select("tbody tr"):
            cells = row.find_all("td")
            if cells and cells[0].get_text(" ", strip=True).rstrip(" +") in labels:
                return self._to_float(cells[-1].get_text())
        return None

    def _three_year_growth(self, soup, title: str) -> Optional[float]:
        for table in soup.select("table.ranges-table"):
            if title in table.get_text():
                match = re.search(r"3 Years:\s*(-?[\d.,]+)\s*%", table.get_text(" ", strip=True))
                if match:
                    return self._to_float(match.group(1))
        return None

    def _fetch_company_page(self, query: str, headers: Dict[str, str]) -> requests.Response:
        """Tries the query as a ticker, then as a company name via screener's search."""
        slug = quote(SCREENER_TICKER_ALIASES.get(query, query), safe="")
        resp = requests.get(f"https://www.screener.in/company/{slug}/consolidated/", headers=headers, timeout=10)
        if resp.status_code == 404:
            resp = requests.get(f"https://www.screener.in/company/{slug}/", headers=headers, timeout=10)
        if resp.status_code == 404:
            search = requests.get("https://www.screener.in/api/company/search/", params={"q": query}, headers=headers, timeout=10)
            search.raise_for_status()
            matches = search.json()
            if matches:
                resp = requests.get(f"https://www.screener.in{matches[0]['url']}", headers=headers, timeout=10)
        return resp

    def _scrape_screener_live(self, ticker: str) -> Dict[str, Any]:
        """Scrapes live company fundamentals, ratios, and primary document links from screener.in."""
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        resp = self._fetch_company_page(ticker, headers)
        if resp.status_code != 200:
            raise Exception(f"Screener returned status {resp.status_code}")

        slug_match = re.search(r"/company/([^/]+)/", resp.url)
        if slug_match:
            ticker = unquote(slug_match.group(1))

        soup = BeautifulSoup(resp.text, "html.parser")
        # Companies without consolidated accounts return an empty consolidated page
        if not soup.select("#profit-loss tbody tr") and "/consolidated/" in resp.url:
            standalone = requests.get(resp.url.replace("consolidated/", ""), headers=headers, timeout=10)
            if standalone.status_code == 200:
                soup = BeautifulSoup(standalone.text, "html.parser")

        company_name_tag = soup.find("h1")
        name = company_name_tag.text.strip() if company_name_tag else ticker

        ratios: Dict[str, float] = {}
        for item in soup.select("#top-ratios li") or soup.select(".company-ratios li"):
            name_el = item.select_one(".name")
            val_el = item.select_one(".value .number") or item.select_one(".value")
            if name_el and val_el:
                value = self._to_float(val_el.text)
                if value is not None:
                    ratios[name_el.text.strip().lower()] = value

        profit_loss = soup.select_one("#profit-loss")
        balance_sheet = soup.select_one("#balance-sheet")
        borrowings = self._latest_row_value(balance_sheet, "Borrowings", "Borrowing")
        equity_capital = self._latest_row_value(balance_sheet, "Equity Capital")
        reserves = self._latest_row_value(balance_sheet, "Reserves")
        debt_to_equity = None
        if borrowings is not None and equity_capital is not None and reserves is not None and equity_capital + reserves > 0:
            debt_to_equity = round(borrowings / (equity_capital + reserves), 2)

        annual_report_links = []
        concall_transcript_links = []

        annual_div = soup.select_one(".annual-reports")
        if annual_div:
            for a_tag in annual_div.find_all("a", href=True):
                title = " ".join(a_tag.text.split())
                if "annual" in title.lower() or "report" in title.lower():
                    annual_report_links.append({"title": title, "url": a_tag["href"]})

        concalls_div = soup.select_one(".concalls")
        if concalls_div:
            for a_tag in concalls_div.find_all("a", href=True):
                parent_text = " ".join(a_tag.parent.text.split()) if a_tag.parent else ""
                link_text = a_tag.text.strip()
                label = f"{parent_text} ({link_text})" if parent_text else link_text
                concall_transcript_links.append({"title": label, "url": a_tag["href"]})

        return {
            "ticker": ticker,
            "company_name": name,
            "data_source": "live_screener",
            "financial_snapshot": {
                "ticker": ticker,
                "company_name": name,
                "ttm_revenue_cr": self._latest_row_value(profit_loss, "Sales", "Revenue"),
                "ebitda_margin_pct": self._latest_row_value(profit_loss, "OPM %"),
                "pat_cr": self._latest_row_value(profit_loss, "Net Profit"),
                "roce_pct": ratios.get("roce"),
                "roe_pct": ratios.get("roe"),
                "pe_ratio": ratios.get("stock p/e"),
                "ev_ebitda": None,
                "sales_cagr_3yr": self._three_year_growth(soup, "Compounded Sales Growth"),
                "profit_cagr_3yr": self._three_year_growth(soup, "Compounded Profit Growth"),
                "debt_to_equity": debt_to_equity,
                "primary_source_notes": f"Live figures from screener.in ({ticker})."
            },
            "primary_documents": {
                "annual_reports": annual_report_links[:5],
                "concall_transcripts": concall_transcript_links[:5]
            },
            "narrative_matrix": {
                "ticker": ticker,
                "company_name": name,
                "coverage_period": "Not assessed",
                "summary_verdict": "Promises vs delivery has not been assessed for this company. Its transcripts are linked in the Primary Vault.",
                "items": []
            },
            "bull_bear_thesis": {
                "ticker": ticker,
                "company_name": name,
                "bull_case": [],
                "bear_case": [],
                "valuation_context": "Not assessed.",
                "primary_source_citations": []
            }
        }


screener_service = ScreenerScraperService()
