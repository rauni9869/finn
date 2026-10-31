export type AnnouncementCategory =
  | 'results'
  | 'M&A'
  | 'fund_raise'
  | 'management_change'
  | 'litigation'
  | 'insider_trading'
  | 'earnings_call'
  | 'investor_meetings'
  | 'credit_rating'
  | 'dividend'
  | 'bonus_split'
  | 'capex'
  | 'press_release'
  | 'postal_ballot'
  | 'agm_egm'
  | 'pledging'
  | 'unclassified';

export type PriorityLevel = 'HIGH' | 'MEDIUM' | 'LOW';

export interface EODMetrics {
  ticker: string;
  symbol: string;
  close: number;
  prev_close: number;
  pct_change: number;
  volume: number;
  avg_volume_20d: number;
  volume_multiple: number;
  timestamp: string;
  is_unusual_volume: boolean;
  is_unusual_price: boolean;
}

export interface StockInfo {
  ticker: string;
  symbol: string;
  name: string;
  sector: string;
  market_cap: string;
  is_portfolio: boolean;
  eod?: EODMetrics | null;
}

export interface MetricDelta {
  val_cr: number;
  qoq_pct?: number;
  yoy_pct?: number;
  margin_pct?: number;
  margin_yoy_bps?: number;
}

export interface QuarterlyResultsEnrichment {
  quarter: string;
  revenue: MetricDelta;
  ebitda: MetricDelta;
  pbt: MetricDelta;
  pat: MetricDelta;
  headline_verdict: string;
  key_highlights: string[];
}

export interface ManagementBioEnrichment {
  incoming_person: string;
  new_role: string;
  effective_date: string;
  predecessor?: string;
  career_profile_bullets: string[];
  strategic_implication: string;
}

export interface CorporateAnnouncement {
  id: string;
  ticker: string;
  company_name: string;
  timestamp: string;
  category: AnnouncementCategory;
  priority: PriorityLevel;
  headline: string;
  details: string;
  one_line_summary: string;
  attachment_url?: string;
  management_enrichment?: ManagementBioEnrichment;
  results_enrichment?: QuarterlyResultsEnrichment;
}

export interface TriggeredAlert {
  id: string;
  ticker: string;
  company_name: string;
  trigger_type: 'VOLUME_SPIKE' | 'PRICE_MOVE' | 'MATERIAL_FILING';
  headline: string;
  detail: string;
  timestamp: string;
  badge_label: string;
  correlated_announcement_id?: string;
  metrics_snapshot?: Record<string, any>;
}

export interface WindowedDigestResponse {
  window_hours: number;
  total_announcements: number;
  high_priority_count: number;
  routine_collapsed_count: number;
  announcements: CorporateAnnouncement[];
  active_alerts: TriggeredAlert[];
  is_sample_data: boolean;
  data_as_of?: string | null;
}

export interface AlertThresholdConfig {
  volume_multiplier_threshold: number;
  price_change_pct_threshold: number;
  material_categories: string[];
}

export interface NarrativeMatrixItem {
  quarter: string;
  management_promised: string;
  actual_delivered: string;
  verdict: 'DELIVERED' | 'MISSED' | 'DELAYED' | 'DIVERGED' | 'PARTIAL';
  verdict_detail: string;
  source_citation: string;
  pdf_page?: number;
}

export interface NarrativeMatrixResponse {
  ticker: string;
  company_name: string;
  coverage_period: string;
  overall_track_record_score: string;
  delivered_pct?: number | null;
  summary_verdict: string;
  items: NarrativeMatrixItem[];
}

export interface FinancialSnapshotResponse {
  ticker: string;
  company_name: string;
  ttm_revenue_cr: number | null;
  ebitda_margin_pct: number | null;
  pat_cr: number | null;
  roce_pct: number | null;
  roe_pct: number | null;
  pe_ratio: number | null;
  ev_ebitda: number | null;
  sales_cagr_3yr: number | null;
  profit_cagr_3yr: number | null;
  debt_to_equity: number | null;
  primary_source_notes: string;
}

export interface BullBearThesisResponse {
  ticker: string;
  company_name: string;
  bull_case: string[];
  bear_case: string[];
  valuation_context: string;
  primary_source_citations: string[];
}

export interface BusinessSegment {
  name: string;
  revenue_share_pct: number;
  growth: string;
}

export interface BusinessSnapshot {
  description: string;
  key_segments: BusinessSegment[];
  export_share_pct?: number;
  domestic_share_pct?: number;
  primary_source: string;
}

export interface BalanceSheetHealth {
  total_debt_cr: number;
  debt_to_equity: number;
  working_capital_days: number;
  contingent_liabilities_cr: number;
  contingent_liabilities_notes: string;
  rpt_flag: boolean;
  rpt_details?: string;
  auditor_qualification_flag: boolean;
  auditor_notes: string;
  primary_source: string;
}

export interface CashQuality {
  cfo_3yr_cumulative_cr: number;
  pat_3yr_cumulative_cr: number;
  cash_conversion_ratio: number;
  fcf_latest_yr_cr: number;
  quality_verdict: string;
  primary_source: string;
}

export interface ManagementGuidance {
  revenue_growth_target: string;
  margin_corridor: string;
  planned_capex_cr: string;
  debt_milestone: string;
  time_horizon: string;
  primary_source: string;
}

export interface PrimaryDocumentItem {
  title: string;
  url: string;
}

export interface PrimaryDocuments {
  annual_reports: PrimaryDocumentItem[];
  concall_transcripts: PrimaryDocumentItem[];
}

export interface FullResearchReport {
  ticker: string;
  company_name: string;
  timestamp: string;
  data_source: 'curated_sample' | 'live_screener';
  financial_snapshot: FinancialSnapshotResponse;
  narrative_matrix: NarrativeMatrixResponse;
  bull_bear_thesis: BullBearThesisResponse;
  primary_documents?: PrimaryDocuments;
  business_snapshot?: BusinessSnapshot;
  balance_sheet?: BalanceSheetHealth;
  cash_quality?: CashQuality;
  guidance?: ManagementGuidance;
}

