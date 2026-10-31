from fastapi import APIRouter, HTTPException
from app.models.schemas import FullResearchReport, NarrativeMatrixResponse, FinancialSnapshotResponse
from app.services.pull.research_engine import research_engine

router = APIRouter(prefix="/research", tags=["Research"])

@router.get("/{ticker}", response_model=FullResearchReport)
def get_company_research(ticker: str):
    """
    On-demand company deep dive grounded 100% in primary filings & transcripts.
    Generalised to any NSE ticker.
    """
    try:
        return research_engine.get_company_deep_dive(ticker)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research generation failed for {ticker}: {str(e)}")

@router.get("/{ticker}/narrative", response_model=NarrativeMatrixResponse)
def get_narrative_vs_numbers(ticker: str):
    """Retrieve 4-quarter promises vs delivery comparison grid with exact citations."""
    report = research_engine.get_company_deep_dive(ticker)
    return report.narrative_matrix

@router.get("/{ticker}/snapshot", response_model=FinancialSnapshotResponse)
def get_financial_snapshot(ticker: str):
    """Retrieve headline financial ratios and margin metrics."""
    report = research_engine.get_company_deep_dive(ticker)
    return report.financial_snapshot

