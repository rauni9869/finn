from fastapi import APIRouter, HTTPException
from app.models.schemas import FullResearchReport, NarrativeMatrixResponse, FinancialSnapshotResponse
from app.services.pull.research_engine import research_engine
from app.services.pull.narrative_analyzer import narrative_analyzer, AnalysisUnavailable
from app.services.data_fetchers.screener_scraper import CompanyDataUnavailable

router = APIRouter(prefix="/research", tags=["Research"])

@router.get("/{ticker}", response_model=FullResearchReport)
def get_company_research(ticker: str):
    """
    On-demand company deep dive grounded 100% in primary filings & transcripts.
    Generalised to any NSE ticker.
    """
    try:
        return research_engine.get_company_deep_dive(ticker)
    except CompanyDataUnavailable as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research generation failed for {ticker}: {str(e)}")

@router.get("/{ticker}/analysis", response_model=NarrativeMatrixResponse)
def get_ai_analysis(ticker: str):
    """AI promises vs delivery from the company's own transcripts and reported results."""
    try:
        return narrative_analyzer.analyze(ticker)
    except AnalysisUnavailable as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/{ticker}/narrative", response_model=NarrativeMatrixResponse)
def get_narrative_vs_numbers(ticker: str):
    """Retrieve 4-quarter promises vs delivery comparison grid with exact citations."""
    return get_company_research(ticker).narrative_matrix

@router.get("/{ticker}/snapshot", response_model=FinancialSnapshotResponse)
def get_financial_snapshot(ticker: str):
    """Retrieve headline financial ratios and margin metrics."""
    return get_company_research(ticker).financial_snapshot

