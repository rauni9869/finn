from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AnnouncementCategory(str, Enum):
    RESULTS = "results"
    MA = "M&A"
    FUND_RAISE = "fund_raise"
    MANAGEMENT_CHANGE = "management_change"
    LITIGATION = "litigation"
    INSIDER_TRADING = "insider_trading"
    EARNINGS_CALL = "earnings_call"
    INVESTOR_MEETINGS = "investor_meetings"
    CREDIT_RATING = "credit_rating"
    DIVIDEND = "dividend"
    BONUS_SPLIT = "bonus_split"
    CAPEX = "capex"
    PRESS_RELEASE = "press_release"
    POSTAL_BALLOT = "postal_ballot"
    AGM_EGM = "agm_egm"
    PLEDGING = "pledging"
    UNCLASSIFIED = "unclassified"


class PriorityLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class DeliveryVerdict(str, Enum):
    DELIVERED = "DELIVERED"
    MISSED = "MISSED"
    DELAYED = "DELAYED"
    DIVERGED = "DIVERGED"
    PARTIAL = "PARTIAL"


# Market EOD data schemas
class EODMetrics(BaseModel):
    ticker: str
    symbol: str
    close: float
    prev_close: float
    pct_change: float
    volume: int
    avg_volume_20d: int
    volume_multiple: float
    timestamp: str
    is_unusual_volume: bool = False
    is_unusual_price: bool = False


# Stock portfolio metadata
class StockInfo(BaseModel):
    ticker: str
    symbol: str
    name: str
    sector: str
    market_cap: str  # Mega, Large, Mid, Small, Micro
    is_portfolio: bool = True
    eod: Optional[EODMetrics] = None


# Push Enrichment Models
class ManagementBioEnrichment(BaseModel):
    incoming_person: str
    new_role: str
    effective_date: str
    predecessor: Optional[str] = None
    career_profile_bullets: List[str] = Field(default_factory=list)
    strategic_implication: str


class MetricDelta(BaseModel):
    val_cr: float
    qoq_pct: Optional[float] = None
    yoy_pct: Optional[float] = None
    margin_pct: Optional[float] = None
    margin_yoy_bps: Optional[float] = None


class QuarterlyResultsEnrichment(BaseModel):
    quarter: str
    revenue: MetricDelta
    ebitda: MetricDelta
    pbt: MetricDelta
    pat: MetricDelta
    headline_verdict: str
    key_highlights: List[str] = Field(default_factory=list)


class CorporateAnnouncement(BaseModel):
    id: str
    ticker: str
    company_name: str
    timestamp: str
    category: AnnouncementCategory
    priority: PriorityLevel
    headline: str
    details: str
    one_line_summary: str
    attachment_url: Optional[str] = None
    management_enrichment: Optional[ManagementBioEnrichment] = None
    results_enrichment: Optional[QuarterlyResultsEnrichment] = None


# Triggered Alert Model
class AlertTriggerType(str, Enum):
    VOLUME_SPIKE = "VOLUME_SPIKE"
    PRICE_MOVE = "PRICE_MOVE"
    MATERIAL_FILING = "MATERIAL_FILING"


class TriggeredAlert(BaseModel):
    id: str
    ticker: str
    company_name: str
    trigger_type: AlertTriggerType
    headline: str
    detail: str
    timestamp: str
    badge_label: str
    correlated_announcement_id: Optional[str] = None
    metrics_snapshot: Optional[Dict[str, Any]] = None


# Alert Configuration Sliders
class AlertThresholdConfig(BaseModel):
    volume_multiplier_threshold: float = 2.0  # e.g., > 2.0x 20-day avg
    price_change_pct_threshold: float = 4.0   # e.g., > ±4% in a day
    material_categories: List[str] = [
        "results", "M&A", "management_change", "litigation", "fund_raise", "capex"
    ]


# Windowed Digest Response
class WindowedDigestResponse(BaseModel):
    window_hours: int
    total_announcements: int
    high_priority_count: int
    routine_collapsed_count: int
    announcements: List[CorporateAnnouncement]
    active_alerts: List[TriggeredAlert] = Field(default_factory=list)
    is_sample_data: bool = True
    data_as_of: Optional[str] = None


# Pull Research Dimensions Schemas
class NarrativeMatrixItem(BaseModel):
    quarter: str
    management_promised: str
    actual_delivered: str
    verdict: DeliveryVerdict
    verdict_detail: str
    source_citation: str
    pdf_page: Optional[int] = None


class NarrativeMatrixResponse(BaseModel):
    ticker: str
    company_name: str
    coverage_period: str
    overall_track_record_score: str  # e.g., "3 of 4 promises delivered"
    delivered_pct: Optional[int] = None  # None when no promises were assessed
    summary_verdict: str
    items: List[NarrativeMatrixItem]


class FinancialSnapshotResponse(BaseModel):
    ticker: str
    company_name: str
    ttm_revenue_cr: Optional[float] = None
    ebitda_margin_pct: Optional[float] = None
    pat_cr: Optional[float] = None
    roce_pct: Optional[float] = None
    roe_pct: Optional[float] = None
    pe_ratio: Optional[float] = None
    ev_ebitda: Optional[float] = None
    sales_cagr_3yr: Optional[float] = None
    profit_cagr_3yr: Optional[float] = None
    debt_to_equity: Optional[float] = None
    primary_source_notes: str


class BullBearThesisResponse(BaseModel):
    ticker: str
    company_name: str
    bull_case: List[str]
    bear_case: List[str]
    valuation_context: str
    primary_source_citations: List[str]


class BusinessSnapshot(BaseModel):
    description: str
    key_segments: List[Dict[str, Any]]  # name, revenue_share_pct, growth
    export_share_pct: Optional[float] = None
    domestic_share_pct: Optional[float] = None
    primary_source: str


class BalanceSheetHealth(BaseModel):
    total_debt_cr: float
    debt_to_equity: float
    working_capital_days: int
    contingent_liabilities_cr: float
    contingent_liabilities_notes: str
    rpt_flag: bool  # Related party transaction flag
    rpt_details: Optional[str] = None
    auditor_qualification_flag: bool
    auditor_notes: str
    primary_source: str


class CashQuality(BaseModel):
    cfo_3yr_cumulative_cr: float
    pat_3yr_cumulative_cr: float
    cash_conversion_ratio: float  # CFO / EBITDA or CFO / PAT
    fcf_latest_yr_cr: float
    quality_verdict: str  # Clean / Caution / Red Flag
    primary_source: str


class ManagementGuidance(BaseModel):
    revenue_growth_target: str
    margin_corridor: str
    planned_capex_cr: str
    debt_milestone: str
    time_horizon: str
    primary_source: str


class PrimaryDocumentItem(BaseModel):
    title: str
    url: str


class PrimaryDocuments(BaseModel):
    annual_reports: List[PrimaryDocumentItem] = []
    concall_transcripts: List[PrimaryDocumentItem] = []


class FullResearchReport(BaseModel):
    ticker: str
    company_name: str
    timestamp: str
    data_source: str  # "curated_sample" (hand-written profile) or "live_screener"
    financial_snapshot: FinancialSnapshotResponse
    narrative_matrix: NarrativeMatrixResponse
    bull_bear_thesis: BullBearThesisResponse
    primary_documents: Optional[PrimaryDocuments] = None
    business_snapshot: Optional[BusinessSnapshot] = None
    balance_sheet: Optional[BalanceSheetHealth] = None
    cash_quality: Optional[CashQuality] = None
    guidance: Optional[ManagementGuidance] = None

