import React, { useState, useEffect } from 'react';
import { 
  FullResearchReport, 
  NarrativeMatrixItem,
  StockInfo 
} from '../types';
import { API_BASE } from '../api';

const show = (value: number | null | undefined, prefix = '', suffix = '') =>
  value === null || value === undefined ? '—' : `${prefix}${value.toLocaleString()}${suffix}`;

interface PullResearchHubProps {
  initialTicker?: string;
  onSelectTicker?: (ticker: string) => void;
}

export const PullResearchHub: React.FC<PullResearchHubProps> = ({
  initialTicker = 'TRENT',
  onSelectTicker,
}) => {
  const [selectedTicker, setSelectedTicker] = useState<string>(initialTicker);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [report, setReport] = useState<FullResearchReport | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeDimensionTab, setActiveDimensionTab] = useState<
    'narrative' | 'financials' | 'thesis' | 'balance_sheet' | 'cash_quality' | 'guidance' | 'documents'
  >('narrative');
  const [selectedCitation, setSelectedCitation] = useState<string | null>(null);

  // Suggested quick tickers: portfolio staples + ad-hoc generalization tickers
  const quickTickers = [
    { ticker: 'TRENT', label: 'Trent Ltd (Fashion/Retail)' },
    { ticker: 'TATAMOTORS', label: 'Tata Motors (Auto/CV/EV)' },
    { ticker: 'POLYCAB', label: 'Polycab (Cables/FMEG)' },
    { ticker: 'DIXON', label: 'Dixon Tech (EMS/Generalisation)' },
    { ticker: 'ZOMATO', label: 'Zomato (Quick Commerce/Ad-hoc)' },
  ];

  useEffect(() => {
    if (initialTicker) {
      setSelectedTicker(initialTicker);
    }
  }, [initialTicker]);

  useEffect(() => {
    fetchResearchReport(selectedTicker);
  }, [selectedTicker]);

  const fetchResearchReport = async (ticker: string) => {
    setLoading(true);
    setError(null);
    setReport(null);
    try {
      const res = await fetch(`${API_BASE}/api/research/${encodeURIComponent(ticker.toUpperCase())}`);
      if (!res.ok) {
        const body = await res.json().catch(() => null);
        throw new Error(body?.detail || `Failed to load research for ${ticker} (HTTP ${res.status})`);
      }
      const data: FullResearchReport = await res.json();
      setReport(data);
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Error connecting to research engine');
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const clean = searchQuery.trim().toUpperCase();
    if (clean) {
      setSelectedTicker(clean);
      if (onSelectTicker) onSelectTicker(clean);
      setSearchQuery('');
    }
  };

  const handleQuickSelect = (ticker: string) => {
    setSelectedTicker(ticker);
    if (onSelectTicker) onSelectTicker(ticker);
  };

  const getVerdictBadge = (verdict: NarrativeMatrixItem['verdict']) => {
    switch (verdict) {
      case 'DELIVERED':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
            ✓ DELIVERED
          </span>
        );
      case 'MISSED':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-rose-500/20 text-rose-400 border border-rose-500/30">
            ✕ MISSED
          </span>
        );
      case 'DELAYED':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-amber-500/20 text-amber-400 border border-amber-500/30">
            ⏱ DELAYED
          </span>
        );
      case 'DIVERGED':
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-purple-500/20 text-purple-400 border border-purple-500/30">
            ⤹ DIVERGED
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-slate-500/20 text-slate-400 border border-slate-500/30">
            {verdict}
          </span>
        );
    }
  };

  return (
    <div className="space-y-4 pb-20">
      {/* Ticker Selector & Search Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-sm">
        <form onSubmit={handleSearchSubmit} className="flex gap-2 mb-3">
          <div className="relative flex-1">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Enter a ticker or company name (e.g. INFY, Tata Steel)..."
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-emerald-500 font-mono"
            />
          </div>
          <button
            type="submit"
            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold rounded-lg transition-colors shadow-sm flex items-center gap-1.5"
          >
            <span>Analyze</span>
          </button>
        </form>

        {/* Quick Ticker Chips */}
        <div className="flex flex-wrap items-center gap-1.5 text-xs">
          <span className="text-slate-500 text-[11px] font-medium mr-1">Quick Picks:</span>
          {quickTickers.map((item) => (
            <button
              key={item.ticker}
              type="button"
              onClick={() => handleQuickSelect(item.ticker)}
              className={`px-2.5 py-1 rounded-md font-mono text-[11px] transition-all ${
                selectedTicker === item.ticker
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/50 font-bold'
                  : 'bg-slate-800 text-slate-400 hover:bg-slate-750 hover:text-slate-200 border border-slate-750'
              }`}
            >
              {item.ticker}
            </button>
          ))}
        </div>
      </div>

      {/* Data Source Notice */}
      {report && !loading && (
        <div className="px-3 py-2 bg-amber-950/30 border border-amber-800/40 rounded-lg text-xs text-amber-200/90">
          {report.data_source === 'curated_sample'
            ? 'Hand-written sample profile for demonstration. Citations and analysis are illustrative and have not been checked against the filings. Ratios and document links update live when available.'
            : 'Live figures and document links from screener.in. Analysis of annual reports and transcripts is not available for this company yet.'}
        </div>
      )}

      {/* Loading Skeleton */}
      {loading && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center space-y-4">
          <div className="inline-block animate-spin h-8 w-8 border-2 border-emerald-500 border-t-transparent rounded-full mb-2"></div>
          <p className="text-sm text-slate-300 font-medium">
            Loading research for <span className="font-mono text-emerald-400">{selectedTicker}</span>...
          </p>
          <p className="text-xs text-slate-500">
            Fetching figures and document links...
          </p>
        </div>
      )}

      {/* Error View */}
      {error && !loading && (
        <div className="bg-rose-950/40 border border-rose-800/50 rounded-xl p-6 text-center space-y-3">
          <div className="text-rose-400 text-sm font-semibold">Failed to load research report</div>
          <p className="text-xs text-slate-400">{error}</p>
          <button
            onClick={() => fetchResearchReport(selectedTicker)}
            className="px-3 py-1.5 bg-rose-600 hover:bg-rose-500 text-white rounded text-xs font-semibold"
          >
            Retry Analysis
          </button>
        </div>
      )}

      {/* Active Research Content */}
      {report && !loading && (
        <div className="space-y-4">
          {/* Company Banner & Scorecard */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 sm:p-5 shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-800">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-lg font-bold text-slate-100">{report.ticker}</span>
                  <span className="text-xs text-slate-400">·</span>
                  <span className="text-sm font-medium text-slate-300">{report.company_name}</span>
                </div>
                <div className="text-xs text-slate-500 mt-0.5">
                  NSE Primary Listing · Research coverage as of {new Date(report.timestamp).toLocaleDateString()}
                </div>
              </div>

              {/* Management Credibility Score badge */}
              <div className="flex items-center gap-3 bg-slate-950 border border-slate-800 px-3 py-2 rounded-lg">
                <div className="text-right">
                  <div className="text-[10px] uppercase tracking-wider text-slate-400 font-medium">
                    Guidance Credibility
                  </div>
                  <div className="text-xs text-slate-300 font-medium">
                    {report.narrative_matrix.overall_track_record_score}
                  </div>
                </div>
                <div className="h-8 w-8 rounded-full bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center font-mono font-bold text-xs text-emerald-400">
                  {report.narrative_matrix.delivered_pct === null || report.narrative_matrix.delivered_pct === undefined ? '—' : `${report.narrative_matrix.delivered_pct}%`}
                </div>
              </div>
            </div>

            {/* Dimension Sub-navigation Tabs */}
            <div className="flex gap-2 overflow-x-auto pt-3 pb-1 scrollbar-thin">
              <button
                type="button"
                onClick={() => setActiveDimensionTab('narrative')}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors flex items-center gap-1.5 ${
                  activeDimensionTab === 'narrative'
                    ? 'bg-emerald-600 text-white shadow-sm font-semibold'
                    : 'bg-slate-800 text-slate-400 hover:text-slate-200'
                }`}
              >
                <span>⚖ Narrative vs Numbers</span>
                <span className="text-[10px] bg-emerald-800/60 px-1.5 py-0.2 rounded font-mono">
                  Flagship
                </span>
              </button>

              <button
                type="button"
                onClick={() => setActiveDimensionTab('financials')}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors ${
                  activeDimensionTab === 'financials'
                    ? 'bg-emerald-600 text-white shadow-sm font-semibold'
                    : 'bg-slate-800 text-slate-400 hover:text-slate-200'
                }`}
              >
                📊 Financial Snapshot
              </button>

              <button
                type="button"
                onClick={() => setActiveDimensionTab('thesis')}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors ${
                  activeDimensionTab === 'thesis'
                    ? 'bg-emerald-600 text-white shadow-sm font-semibold'
                    : 'bg-slate-800 text-slate-400 hover:text-slate-200'
                }`}
              >
                🐂 Bull vs Bear
              </button>

              <button
                type="button"
                onClick={() => setActiveDimensionTab('balance_sheet')}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors ${
                  activeDimensionTab === 'balance_sheet'
                    ? 'bg-emerald-600 text-white shadow-sm font-semibold'
                    : 'bg-slate-800 text-slate-400 hover:text-slate-200'
                }`}
              >
                🛡 Balance Sheet & RPT
              </button>

              <button
                type="button"
                onClick={() => setActiveDimensionTab('cash_quality')}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors ${
                  activeDimensionTab === 'cash_quality'
                    ? 'bg-emerald-600 text-white shadow-sm font-semibold'
                    : 'bg-slate-800 text-slate-400 hover:text-slate-200'
                }`}
              >
                💧 Cash Quality
              </button>

              <button
                type="button"
                onClick={() => setActiveDimensionTab('guidance')}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors ${
                  activeDimensionTab === 'guidance'
                    ? 'bg-emerald-600 text-white shadow-sm font-semibold'
                    : 'bg-slate-800 text-slate-400 hover:text-slate-200'
                }`}
              >
                🎯 Guidance Tracker
              </button>

              <button
                type="button"
                onClick={() => setActiveDimensionTab('documents')}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-colors flex items-center gap-1.5 ${
                  activeDimensionTab === 'documents'
                    ? 'bg-emerald-600 text-white shadow-sm font-semibold'
                    : 'bg-slate-800 text-slate-400 hover:text-slate-200'
                }`}
              >
                <span>📑 Primary Vault</span>
                {report.primary_documents && (
                  <span className="text-[10px] bg-slate-950/70 text-emerald-300 px-1.5 py-0.2 rounded font-mono">
                    {report.primary_documents.annual_reports.length + report.primary_documents.concall_transcripts.length}
                  </span>
                )}
              </button>
            </div>
          </div>

          {/* TAB 1: FLAGSHIP NARRATIVE VS NUMBERS MATRIX */}
          {activeDimensionTab === 'narrative' && (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 sm:p-5 space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div>
                  <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                    <span>Narrative vs Numbers Matrix</span>
                    <span className="text-[11px] font-normal text-slate-400">
                      (Promises vs Delivery)
                    </span>
                  </h3>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Reconciling management claims in concalls against hard numbers reported in subsequent quarters.
                  </p>
                </div>
                <div className="text-xs font-mono bg-slate-950 border border-slate-800 px-2.5 py-1 rounded text-slate-300">
                  Coverage: {report.narrative_matrix.coverage_period}
                </div>
              </div>

              {/* Summary synthesis */}
              <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-xs text-slate-300 leading-relaxed">
                <span className="font-semibold text-emerald-400">Analyst Verdict: </span>
                {report.narrative_matrix.summary_verdict}
              </div>

              {/* 4-Quarter Comparison Table */}
              {report.narrative_matrix.items.length > 0 && <div className="overflow-x-auto">
                <table className="w-full text-left text-xs border-collapse">
                  <thead>
                    <tr className="border-b border-slate-800 text-slate-400 font-medium">
                      <th className="py-2.5 px-3 w-24">Quarter</th>
                      <th className="py-2.5 px-3">Management Promise / Narrative</th>
                      <th className="py-2.5 px-3">Actual Delivered / Financial Reality</th>
                      <th className="py-2.5 px-3 w-28 text-center">Outcome</th>
                      <th className="py-2.5 px-3 w-36">Primary Citation</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 font-sans">
                    {report.narrative_matrix.items.map((item, idx) => (
                      <tr key={idx} className="hover:bg-slate-850/40 transition-colors">
                        <td className="py-3 px-3 font-mono font-semibold text-slate-200 align-top whitespace-nowrap">
                          {item.quarter}
                        </td>
                        <td className="py-3 px-3 text-slate-300 leading-relaxed align-top">
                          <p className="italic text-slate-300">"{item.management_promised}"</p>
                        </td>
                        <td className="py-3 px-3 text-slate-200 leading-relaxed align-top">
                          <p>{item.actual_delivered}</p>
                          <div className="text-[11px] text-slate-400 mt-1">
                            {item.verdict_detail}
                          </div>
                        </td>
                        <td className="py-3 px-3 text-center align-top whitespace-nowrap">
                          {getVerdictBadge(item.verdict)}
                        </td>
                        <td className="py-3 px-3 font-mono text-[11px] text-slate-400 align-top">
                          <button
                            type="button"
                            onClick={() => setSelectedCitation(item.source_citation)}
                            className="text-left text-emerald-400 hover:text-emerald-300 hover:underline flex items-start gap-1"
                          >
                            <span>📎</span>
                            <span>{item.source_citation}</span>
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>}

              {/* Citation Modal / Drawer if clicked */}
              {selectedCitation && (
                <div className="bg-slate-950 border border-emerald-800/40 rounded-lg p-3 text-xs flex items-center justify-between">
                  <div className="flex items-center gap-2 text-slate-300">
                    <span className="text-emerald-400 font-semibold">Primary Reference:</span>
                    <span className="font-mono text-slate-200">{selectedCitation}</span>
                    
                  </div>
                  <button
                    onClick={() => setSelectedCitation(null)}
                    className="text-slate-400 hover:text-slate-200 text-xs px-2 py-0.5"
                  >
                    Dismiss
                  </button>
                </div>
              )}
            </div>
          )}

          {/* TAB 2: FINANCIAL SNAPSHOT */}
          {activeDimensionTab === 'financials' && (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 sm:p-5 space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-bold text-slate-100">
                  Financial Performance & Capital Efficiency Ratios
                </h3>
                <span className="text-xs font-mono text-slate-500">TTM</span>
              </div>

              {/* 8-Grid Metric Cards */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
                  <div className="text-[11px] text-slate-400 font-medium">TTM Revenue</div>
                  <div className="text-base font-bold font-mono text-slate-100 mt-1">
                    {show(report.financial_snapshot.ttm_revenue_cr, '₹', ' Cr')}
                  </div>
                  <div className="text-[10px] text-emerald-400 mt-1">
                    3Y CAGR: {show(report.financial_snapshot.sales_cagr_3yr, '', '%')}
                  </div>
                </div>

                <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
                  <div className="text-[11px] text-slate-400 font-medium">EBITDA Margin</div>
                  <div className="text-base font-bold font-mono text-slate-100 mt-1">
                    {show(report.financial_snapshot.ebitda_margin_pct, '', '%')}
                  </div>
                  <div className="text-[10px] text-slate-500 mt-1">Operating margin</div>
                </div>

                <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
                  <div className="text-[11px] text-slate-400 font-medium">TTM PAT</div>
                  <div className="text-base font-bold font-mono text-slate-100 mt-1">
                    {show(report.financial_snapshot.pat_cr, '₹', ' Cr')}
                  </div>
                  <div className="text-[10px] text-emerald-400 mt-1">
                    3Y Profit CAGR: {show(report.financial_snapshot.profit_cagr_3yr, '', '%')}
                  </div>
                </div>

                <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
                  <div className="text-[11px] text-slate-400 font-medium">ROCE / ROE</div>
                  <div className="text-base font-bold font-mono text-slate-100 mt-1">
                    {show(report.financial_snapshot.roce_pct, '', '%')} / {show(report.financial_snapshot.roe_pct, '', '%')}
                  </div>
                  <div className="text-[10px] text-slate-400 mt-1">Return on capital / equity</div>
                </div>

                <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
                  <div className="text-[11px] text-slate-400 font-medium">P/E Multiple</div>
                  <div className="text-base font-bold font-mono text-slate-100 mt-1">
                    {show(report.financial_snapshot.pe_ratio, '', 'x')}
                  </div>
                  <div className="text-[10px] text-slate-400 mt-1">Based on TTM EPS</div>
                </div>

                <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
                  <div className="text-[11px] text-slate-400 font-medium">EV / EBITDA</div>
                  <div className="text-base font-bold font-mono text-slate-100 mt-1">
                    {show(report.financial_snapshot.ev_ebitda, '', 'x')}
                  </div>
                  <div className="text-[10px] text-slate-400 mt-1">Enterprise Multiple</div>
                </div>

                <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
                  <div className="text-[11px] text-slate-400 font-medium">Debt to Equity</div>
                  <div className="text-base font-bold font-mono text-slate-100 mt-1">
                    {show(report.financial_snapshot.debt_to_equity, '', 'x')}
                  </div>
                  <div className="text-[10px] text-slate-400 mt-1">
                    Latest balance sheet
                  </div>
                </div>

                <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
                  <div className="text-[11px] text-slate-400 font-medium">Primary Source</div>
                  <div className="text-[11px] font-mono text-slate-300 mt-1 truncate">
                    {report.financial_snapshot.primary_source_notes}
                  </div>
                  
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: BULL VS BEAR THESIS */}
          {activeDimensionTab === 'thesis' && (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 sm:p-5 space-y-4">
              <div>
                <h3 className="text-sm font-bold text-slate-100">Bull vs Bear</h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  A short case each way.
                </p>
              </div>

              {report.bull_bear_thesis.bull_case.length === 0 && report.bull_bear_thesis.bear_case.length === 0 ? (
                <div className="text-xs text-slate-500">Not assessed for this company yet.</div>
              ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Bull Box */}
                <div className="bg-emerald-950/20 border border-emerald-900/40 rounded-xl p-4 space-y-3">
                  <div className="flex items-center gap-2 text-emerald-400 font-bold text-xs uppercase tracking-wider">
                    <span>🐂 The Bull Thesis</span>
                  </div>
                  <ul className="space-y-2 text-xs text-slate-300">
                    {report.bull_bear_thesis.bull_case.map((point, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-emerald-500 font-bold">›</span>
                        <span className="leading-relaxed">{point}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Bear Box */}
                <div className="bg-rose-950/20 border border-rose-900/40 rounded-xl p-4 space-y-3">
                  <div className="flex items-center gap-2 text-rose-400 font-bold text-xs uppercase tracking-wider">
                    <span>🐻 The Bear Thesis & Risks</span>
                  </div>
                  <ul className="space-y-2 text-xs text-slate-300">
                    {report.bull_bear_thesis.bear_case.map((point, idx) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-rose-500 font-bold">›</span>
                        <span className="leading-relaxed">{point}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
              )}

              {/* Valuation & Citation Notes */}
              <div className="bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs space-y-2">
                <div className="flex items-center justify-between text-slate-400">
                  <span className="font-semibold text-slate-300">Valuation Context:</span>
                  <span className="font-mono text-slate-400">{report.bull_bear_thesis.valuation_context}</span>
                </div>
                <div className="text-[11px] text-slate-500">
                  <span className="font-medium text-slate-400">Source Footnotes: </span>
                  {report.bull_bear_thesis.primary_source_citations.join(' · ')}
                </div>
              </div>
            </div>
          )}

          {/* TAB 4: BALANCE SHEET HEALTH & RPTs */}
          {activeDimensionTab === 'balance_sheet' && (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 sm:p-5 space-y-4">
              <div>
                <h3 className="text-sm font-bold text-slate-100">
                  Balance Sheet Health, Governance & Contingencies
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Auditor report scrutiny, Related Party Transactions (RPT) audit, and working capital cycle.
                </p>
              </div>

              {report.balance_sheet ? (
                <div className="space-y-4">
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
                      <div className="text-[11px] text-slate-400">Total Borrowings</div>
                      <div className="text-base font-bold font-mono text-slate-100 mt-1">
                        ₹{report.balance_sheet.total_debt_cr} Cr
                      </div>
                      <div className="text-[10px] text-slate-400 mt-1">
                        D/E: {report.balance_sheet.debt_to_equity}x
                      </div>
                    </div>

                    <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
                      <div className="text-[11px] text-slate-400">Working Capital Cycle</div>
                      <div className="text-base font-bold font-mono text-slate-100 mt-1">
                        {report.balance_sheet.working_capital_days} Days
                      </div>
                      
                    </div>

                    <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
                      <div className="text-[11px] text-slate-400">Contingent Liabilities</div>
                      <div className="text-base font-bold font-mono text-slate-100 mt-1">
                        ₹{report.balance_sheet.contingent_liabilities_cr} Cr
                      </div>
                      <div className="text-[10px] text-slate-500 mt-1 truncate">
                        {report.balance_sheet.contingent_liabilities_notes}
                      </div>
                    </div>

                    <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
                      <div className="text-[11px] text-slate-400">Auditor Opinion</div>
                      <div className="mt-1">
                        {!report.balance_sheet.auditor_qualification_flag ? (
                          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                            ✓ Unqualified (Clean)
                          </span>
                        ) : (
                          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-rose-500/20 text-rose-400 border border-rose-500/30">
                            ⚠ Qualified Opinion
                          </span>
                        )}
                      </div>
                      <div className="text-[10px] text-slate-400 mt-1 truncate">
                        {report.balance_sheet.auditor_notes}
                      </div>
                    </div>
                  </div>

                  {/* Related Party Transactions (RPT) Scrutiny Card */}
                  <div className={`p-4 rounded-xl border ${
                    report.balance_sheet.rpt_flag 
                      ? 'bg-amber-950/20 border-amber-900/50' 
                      : 'bg-slate-950 border-slate-800'
                  }`}>
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold text-slate-200">
                          Related Party Transactions (RPT) Audit
                        </span>
                        {report.balance_sheet.rpt_flag ? (
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">
                            Attention Required
                          </span>
                        ) : (
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                            Arm's Length / Normal Course
                          </span>
                        )}
                      </div>
                      <span className="text-[11px] font-mono text-slate-500">
                        Primary Source: {report.balance_sheet.primary_source}
                      </span>
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed">
                      {report.balance_sheet.rpt_details || 'All material RPT transactions verified within statutory arm\'s-length approval corridors.'}
                    </p>
                  </div>
                </div>
              ) : (
                <div className="text-xs text-slate-500">Not available for this company yet. See the debt-to-equity figure in Financial Snapshot.</div>
              )}
            </div>
          )}

          {/* TAB 5: CASH QUALITY & CONVERSION */}
          {activeDimensionTab === 'cash_quality' && (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 sm:p-5 space-y-4">
              <div>
                <h3 className="text-sm font-bold text-slate-100">
                  Cash Flow Quality & Conversion Audit
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Validating whether reported accounting profits convert to real cash in the bank (CFO / PAT).
                </p>
              </div>

              {report.cash_quality ? (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                    <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
                      <div className="text-[11px] text-slate-400">3-Year Cumulative CFO</div>
                      <div className="text-base font-bold font-mono text-slate-100 mt-1">
                        ₹{report.cash_quality.cfo_3yr_cumulative_cr.toLocaleString()} Cr
                      </div>
                      <div className="text-[10px] text-slate-500 mt-1">Cash flow from operations</div>
                    </div>

                    <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
                      <div className="text-[11px] text-slate-400">3-Year Cumulative PAT</div>
                      <div className="text-base font-bold font-mono text-slate-100 mt-1">
                        ₹{report.cash_quality.pat_3yr_cumulative_cr.toLocaleString()} Cr
                      </div>
                      <div className="text-[10px] text-slate-500 mt-1">Reported net profit</div>
                    </div>

                    <div className="bg-slate-950 border border-slate-800 p-3 rounded-lg">
                      <div className="text-[11px] text-slate-400">Cash Conversion Ratio</div>
                      <div className="text-base font-bold font-mono text-emerald-400 mt-1">
                        {report.cash_quality.cash_conversion_ratio.toFixed(2)}x
                      </div>
                      <div className={`text-[10px] mt-1 ${report.cash_quality.cash_conversion_ratio >= 0.8 ? 'text-emerald-400' : 'text-amber-400'}`}>
                        {report.cash_quality.cash_conversion_ratio >= 0.8 ? '✓ CFO / PAT at or above 0.8x' : '⚠ CFO / PAT below 0.8x'}
                      </div>
                    </div>
                  </div>

                  <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl text-xs space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-slate-200">Free Cash Flow (FCF) Latest FY:</span>
                      <span className="font-mono font-bold text-slate-100">
                        ₹{report.cash_quality.fcf_latest_yr_cr.toLocaleString()} Cr
                      </span>
                    </div>
                    <div className="text-slate-400 leading-relaxed">
                      <span className="font-semibold text-emerald-400">Audit Finding: </span>
                      {report.cash_quality.quality_verdict}
                    </div>
                    <div className="text-[11px] text-slate-500 pt-1">
                      Primary Source: {report.cash_quality.primary_source}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="text-xs text-slate-500">Not available for this company yet.</div>
              )}
            </div>
          )}

          {/* TAB 6: MANAGEMENT GUIDANCE TRACKER */}
          {activeDimensionTab === 'guidance' && (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 sm:p-5 space-y-4">
              <div>
                <h3 className="text-sm font-bold text-slate-100">
                  Explicit Forward Guidance & Management Commitments
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Statements on forward growth, margin corridors, and planned capital expenditure from concalls.
                </p>
              </div>

              {report.guidance ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
                    <div className="text-[11px] text-slate-400 font-medium">Revenue Growth Outlook</div>
                    <div className="text-sm font-bold text-slate-100">
                      {report.guidance.revenue_growth_target}
                    </div>
                  </div>

                  <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
                    <div className="text-[11px] text-slate-400 font-medium">Target Margin Corridor</div>
                    <div className="text-sm font-bold text-slate-100">
                      {report.guidance.margin_corridor}
                    </div>
                  </div>

                  <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
                    <div className="text-[11px] text-slate-400 font-medium">Capex Budget & Allocation</div>
                    <div className="text-sm font-bold text-slate-100">
                      {report.guidance.planned_capex_cr}
                    </div>
                  </div>

                  <div className="bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-1">
                    <div className="text-[11px] text-slate-400 font-medium">Balance Sheet / Debt Milestone</div>
                    <div className="text-sm font-bold text-slate-100">
                      {report.guidance.debt_milestone}
                    </div>
                  </div>

                  <div className="sm:col-span-2 bg-slate-950 border border-slate-800 p-3 rounded-lg text-xs text-slate-400 flex items-center justify-between">
                    <span>
                      Horizon: <span className="font-semibold text-slate-200">{report.guidance.time_horizon}</span>
                    </span>
                    <span className="font-mono text-[11px] text-slate-500">
                      Primary Source: {report.guidance.primary_source}
                    </span>
                  </div>
                </div>
              ) : (
                <div className="text-xs text-slate-500">Not available for this company yet.</div>
              )}
            </div>
          )}

          {/* TAB 7: PRIMARY SOURCES & FILINGS VAULT */}
          {activeDimensionTab === 'documents' && (
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 sm:p-5 space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div>
                  <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                    <span>Primary Sources Vault</span>
                  </h3>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Direct access to official exchange PDF filings, annual reports, and concall recordings.
                  </p>
                </div>
              </div>

              {report.primary_documents ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Annual Reports Card */}
                  <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-3">
                    <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                      <span className="text-xs font-bold text-slate-200 flex items-center gap-1.5">
                        <span>📑</span>
                        <span>Audited Annual Reports (ARs)</span>
                      </span>
                      <span className="text-[10px] font-mono bg-slate-800 text-slate-300 px-2 py-0.5 rounded">
                        {report.primary_documents.annual_reports.length} Filed
                      </span>
                    </div>

                    {report.primary_documents.annual_reports.length > 0 ? (
                      <ul className="space-y-2">
                        {report.primary_documents.annual_reports.map((doc, idx) => (
                          <li key={idx} className="bg-slate-900/60 border border-slate-800/80 rounded-lg p-2.5 flex items-center justify-between hover:border-emerald-500/40 transition-colors">
                            <div className="flex items-center gap-2 truncate">
                              <span className="text-red-400 font-mono text-xs">AR</span>
                              <span className="text-xs text-slate-200 font-medium truncate">{doc.title}</span>
                            </div>
                            <a
                              href={doc.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="px-2.5 py-1 bg-emerald-600/20 hover:bg-emerald-600 text-emerald-300 hover:text-white rounded text-[11px] font-medium transition-all ml-2 whitespace-nowrap flex items-center gap-1"
                            >
                              <span>Open</span>
                              <span>↗</span>
                            </a>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-xs text-slate-500 italic">No annual reports found in feed.</p>
                    )}
                  </div>

                  {/* Concall Transcripts & Investor Decks Card */}
                  <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-3">
                    <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                      <span className="text-xs font-bold text-slate-200 flex items-center gap-1.5">
                        <span>🎙</span>
                        <span>Earnings Calls & Investor Decks</span>
                      </span>
                      <span className="text-[10px] font-mono bg-slate-800 text-slate-300 px-2 py-0.5 rounded">
                        {report.primary_documents.concall_transcripts.length} Available
                      </span>
                    </div>

                    {report.primary_documents.concall_transcripts.length > 0 ? (
                      <ul className="space-y-2">
                        {report.primary_documents.concall_transcripts.map((doc, idx) => (
                          <li key={idx} className="bg-slate-900/60 border border-slate-800/80 rounded-lg p-2.5 flex items-center justify-between hover:border-emerald-500/40 transition-colors">
                            <div className="flex items-center gap-2 truncate">
                              <span className="text-indigo-400 font-mono text-xs">
                                {doc.url.endsWith('.mp3') ? 'AUDIO' : 'DOC'}
                              </span>
                              <span className="text-xs text-slate-200 font-medium truncate">{doc.title}</span>
                            </div>
                            <a
                              href={doc.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="px-2.5 py-1 bg-indigo-600/20 hover:bg-indigo-600 text-indigo-300 hover:text-white rounded text-[11px] font-medium transition-all ml-2 whitespace-nowrap flex items-center gap-1"
                            >
                              <span>{doc.url.endsWith('.mp3') ? 'Listen' : 'Read'}</span>
                              <span>↗</span>
                            </a>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-xs text-slate-500 italic">No concalls found in feed.</p>
                    )}
                  </div>
                </div>
              ) : (
                <div className="text-xs text-slate-500">No document links available for this company.</div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

