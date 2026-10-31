import hashlib
import io
import json
import logging
import re
import threading
import time
from typing import Any, Dict, List, Optional

import requests
from pydantic import BaseModel
from pypdf import PdfReader

from app.core.config import CACHE_DIR
from app.models.schemas import DeliveryVerdict, NarrativeMatrixItem, NarrativeMatrixResponse
from app.services.data_fetchers.screener_scraper import screener_service
from app.services.llm.router import llm_router

logger = logging.getLogger(__name__)

MAX_TRANSCRIPTS = 4
MAX_CHARS_PER_TRANSCRIPT = 70000
CACHE_TTL_SECONDS = 7 * 24 * 3600

SYSTEM_INSTRUCTION = """You audit Indian listed companies. Compare what management promised on earnings calls with what was later delivered.

Rules:
- Use ONLY the transcripts and quarterly results provided. Never use outside knowledge of the company.
- Pick up to 6 specific, checkable promises about growth, margins, capex, debt, launches or expansion. Prefer promises with numbers or dates.
- Include a promise only if a LATER transcript or the quarterly results show the outcome. Skip promises that cannot be checked yet.
- "quote" must be copied word for word from the transcript page you cite, 8 to 30 words, with no edits.
- "promise_transcript" must exactly match a transcript label, and "page" must be the page holding the quote.
- Verdicts: DELIVERED (met or beaten), PARTIAL (partly met), DELAYED (late but still on track), MISSED (not met), DIVERGED (outcome contradicts the story).
- If the evidence does not clearly support DELIVERED, do not use DELIVERED.
- "actual_delivered" must state the outcome with its numbers and where they came from.
- Be concise and do not flatter management."""


class CheckedPromise(BaseModel):
    promise_transcript: str
    page: int
    quote: str
    management_promised: str
    actual_delivered: str
    verdict: DeliveryVerdict
    verdict_detail: str


class AnalysisOutput(BaseModel):
    summary_verdict: str
    promises: List[CheckedPromise]


class AnalysisUnavailable(Exception):
    """The analysis could not be produced, and the reason is safe to show."""


def _normalise(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


class NarrativeAnalyzer:
    """Builds promises vs delivery from a company's own transcripts and reported quarterly results."""

    def __init__(self):
        self._locks: Dict[str, threading.Lock] = {}
        self._locks_guard = threading.Lock()

    def analyze(self, ticker: str) -> NarrativeMatrixResponse:
        if not llm_router.is_available():
            raise AnalysisUnavailable("AI analysis is not configured on this server.")

        inputs = screener_service.get_analysis_inputs(ticker)
        if not inputs or not inputs["transcripts"]:
            raise AnalysisUnavailable("No earnings call transcripts were found for this company.")

        # One run per company, so repeat requests wait and then read the cache
        with self._lock_for(inputs["ticker"]):
            cached = self._read_cache(inputs)
            if cached:
                return cached
            result = self._run(inputs)
            self._write_cache(inputs, result)
            return result

    def _lock_for(self, ticker: str) -> threading.Lock:
        with self._locks_guard:
            return self._locks.setdefault(ticker, threading.Lock())

    def _run(self, inputs: Dict[str, Any]) -> NarrativeMatrixResponse:
        transcripts = self._load_transcripts(inputs["transcripts"])
        if len(transcripts) < 2:
            raise AnalysisUnavailable("Fewer than two transcripts could be read, so promises can't be checked against later results.")

        sections = []
        for t in transcripts:
            pages = "\n".join(f"[{t['label']} | page {n}]\n{text}" for n, text in sorted(t["pages"].items()))
            sections.append(pages[:MAX_CHARS_PER_TRANSCRIPT])
        labels = ", ".join(t["label"] for t in transcripts)
        prompt = (
            f"Company: {inputs['company_name']} ({inputs['ticker']})\n"
            f"Transcript labels, oldest first: {labels}\n\n"
            f"REPORTED QUARTERLY RESULTS (Rs crore)\n{inputs['quarterly_results']}\n\n"
            "TRANSCRIPTS\n" + "\n\n".join(sections)
        )
        raw = llm_router.generate_content(
            prompt,
            system_instruction=SYSTEM_INSTRUCTION,
            config={"response_mime_type": "application/json", "response_schema": AnalysisOutput, "temperature": 0}
        )
        if not raw:
            raise AnalysisUnavailable("The AI service is busy or its free limit was reached. Please try again in a few minutes.")
        try:
            output = AnalysisOutput.model_validate_json(raw)
        except ValueError as e:
            logger.warning(f"Unreadable analysis output for {inputs['ticker']}: {e}")
            raise AnalysisUnavailable("The AI service returned an unreadable answer. Please try again.")

        items = self._keep_verified(output.promises, transcripts)
        logger.info(f"{inputs['ticker']}: kept {len(items)} of {len(output.promises)} promises after quote checks")
        if not items:
            raise AnalysisUnavailable("No promise could be verified against the transcript text.")

        delivered = sum(1 for i in items if i.verdict == DeliveryVerdict.DELIVERED)
        return NarrativeMatrixResponse(
            ticker=inputs["ticker"],
            company_name=inputs["company_name"],
            coverage_period=f"{transcripts[0]['label']} to {transcripts[-1]['label']} transcripts",
            overall_track_record_score=f"{delivered} of {len(items)} promises delivered",
            delivered_pct=round(delivered / len(items) * 100),
            summary_verdict=output.summary_verdict,
            items=items
        )

    def _load_transcripts(self, links: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}
        transcripts = []
        for link in links[:MAX_TRANSCRIPTS]:
            try:
                resp = requests.get(link["url"], headers=headers, timeout=30)
                resp.raise_for_status()
                reader = PdfReader(io.BytesIO(resp.content))
                pages = {n: page.extract_text() or "" for n, page in enumerate(reader.pages, start=1)}
                if sum(len(text) for text in pages.values()) > 1000:
                    transcripts.append({"label": link["period"], "url": link["url"], "pages": pages})
            except Exception as e:
                logger.warning(f"Could not read transcript {link['period']}: {e}")
        # Screener lists newest first; the model reads oldest first
        return list(reversed(transcripts))

    def _keep_verified(self, promises: List[CheckedPromise], transcripts: List[Dict[str, Any]]) -> List[NarrativeMatrixItem]:
        """Drops any promise whose quote isn't really on the cited transcript page."""
        by_label = {t["label"]: t for t in transcripts}
        items = []
        for p in promises:
            transcript = by_label.get(p.promise_transcript)
            if not transcript:
                continue
            # Allow the next page too, for a quote that runs across a page break
            cited = transcript["pages"].get(p.page, "") + transcript["pages"].get(p.page + 1, "")
            if len(_normalise(p.quote)) < 20 or _normalise(p.quote) not in _normalise(cited):
                continue
            items.append(NarrativeMatrixItem(
                quarter=p.promise_transcript,
                management_promised=p.management_promised,
                actual_delivered=p.actual_delivered,
                verdict=p.verdict,
                verdict_detail=p.verdict_detail,
                source_citation=f"{p.promise_transcript} transcript, p. {p.page}",
                pdf_page=p.page,
                source_url=transcript["url"],
                quote=p.quote
            ))
        return items

    def _cache_path(self, inputs: Dict[str, Any]):
        # A new transcript changes the key, so the analysis refreshes after each call
        key = hashlib.sha256(f"{inputs['ticker']}|{inputs['transcripts'][0]['url']}".encode()).hexdigest()[:24]
        return CACHE_DIR / f"analysis_{key}.json"

    def _read_cache(self, inputs: Dict[str, Any]) -> Optional[NarrativeMatrixResponse]:
        path = self._cache_path(inputs)
        try:
            if time.time() - path.stat().st_mtime < CACHE_TTL_SECONDS:
                return NarrativeMatrixResponse.model_validate_json(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
        return None

    def _write_cache(self, inputs: Dict[str, Any], result: NarrativeMatrixResponse) -> None:
        try:
            self._cache_path(inputs).write_text(result.model_dump_json(), encoding="utf-8")
        except OSError as e:
            logger.warning(f"Could not cache analysis: {e}")


narrative_analyzer = NarrativeAnalyzer()
