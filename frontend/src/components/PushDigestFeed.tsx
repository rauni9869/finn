import React, { useState } from 'react';
import { 
  TrendingUp, TrendingDown, ChevronDown, ChevronUp, FileText, 
  ExternalLink, Sparkles, Building2, UserCheck, AlertCircle, ArrowUpRight, ArrowDownRight, Info
} from 'lucide-react';
import { CorporateAnnouncement, TriggeredAlert, PriorityLevel } from '../types';

interface PushDigestFeedProps {
  announcements: CorporateAnnouncement[];
  alerts: TriggeredAlert[];
  windowHours: number;
  onSelectWindow: (hours: number) => void;
  onSelectStockForResearch: (ticker: string) => void;
}

export const PushDigestFeed: React.FC<PushDigestFeedProps> = ({
  announcements,
  alerts,
  windowHours,
  onSelectWindow,
  onSelectStockForResearch
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [showRoutineCollapsed, setShowRoutineCollapsed] = useState<boolean>(false);
  const [expandedWhyCare, setExpandedWhyCare] = useState<Record<string, boolean>>({});

  const toggleWhyCare = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setExpandedWhyCare(prev => ({ ...prev, [id]: !prev[id] }));
  };

  // Filter announcements
  const highPriority = announcements.filter(a => a.priority === 'HIGH');
  const mediumPriority = announcements.filter(a => a.priority === 'MEDIUM');
  const routineFilings = announcements.filter(a => a.priority === 'LOW');

  const displayedAnnouncements = announcements.filter(a => {
    if (selectedCategory === 'ALL') return true;
    return a.category.toLowerCase() === selectedCategory.toLowerCase();
  });

  const materialList = displayedAnnouncements.filter(a => a.priority !== 'LOW');
  const routineList = displayedAnnouncements.filter(a => a.priority === 'LOW');

  return (
    <div className="space-y-4 pb-20">
      {/* Window Selector Tabs & Quick Category Filter */}
      <div className="bg-gray-900/90 rounded-2xl p-3 border border-gray-800 shadow-md">
        <div className="flex items-center justify-between gap-2 mb-2.5">
          <span className="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">
            Digest Window
          </span>
          <div className="flex items-center gap-1 bg-gray-950 p-1 rounded-xl border border-gray-800">
            {[
              { label: '24h', hours: 24 },
              { label: '48h', hours: 48 },
              { label: '7 Days', hours: 168 }
            ].map(w => (
              <button
                key={w.hours}
                onClick={() => onSelectWindow(w.hours)}
                className={`text-xs px-2.5 py-1 rounded-lg font-medium transition-all ${
                  windowHours === w.hours
                    ? 'bg-blue-600 text-white font-semibold shadow-sm'
                    : 'text-gray-400 hover:text-gray-200'
                }`}
              >
                {w.label}
              </button>
            ))}
          </div>
        </div>

        {/* Category Pills Bar */}
        <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar py-1">
          {['ALL', 'results', 'management_change', 'M&A', 'capex', 'dividend'].map(cat => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`text-[11px] uppercase tracking-wide px-2.5 py-1 rounded-lg whitespace-nowrap font-medium transition-colors ${
                selectedCategory === cat
                  ? 'bg-gray-800 text-blue-400 border border-blue-500/30'
                  : 'bg-gray-950 text-gray-400 border border-gray-800/80 hover:text-gray-300'
              }`}
            >
              {cat === 'ALL' ? 'All Signals' : cat.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Active Triggered Anomalies Header Banner (if any) */}
      {alerts.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center justify-between px-1">
            <span className="text-xs font-bold text-amber-400 flex items-center gap-1.5 uppercase tracking-wider">
              <span className="w-2 h-2 rounded-full bg-amber-400 animate-ping"></span>
              Threshold Triggered Alerts ({alerts.length})
            </span>
          </div>

          <div className="space-y-2">
            {alerts.map(alert => (
              <div
                key={alert.id}
                onClick={() => onSelectStockForResearch(alert.ticker)}
                className="p-3.5 rounded-2xl bg-gradient-to-r from-amber-950/40 via-gray-900 to-gray-900 border border-amber-800/50 hover:border-amber-600/70 transition-all cursor-pointer shadow-lg active:scale-99"
              >
                <div className="flex items-start justify-between gap-2 mb-1">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-sm text-white">{alert.ticker}</span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-900/60 border border-amber-700/60 text-amber-200 font-bold">
                      {alert.badge_label}
                    </span>
                  </div>
                  <span className="text-[10px] text-gray-400 font-mono">
                    {alert.trigger_type.replace('_', ' ')}
                  </span>
                </div>
                <p className="text-xs font-medium text-amber-100/90 leading-snug">
                  {alert.headline}
                </p>
                <p className="text-[11px] text-gray-400 mt-1 leading-relaxed">
                  {alert.detail}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Primary Prioritized Feed */}
      <div className="space-y-3">
        <div className="flex items-center justify-between px-1">
          <span className="text-xs font-bold text-gray-300 uppercase tracking-wider flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-blue-400" />
            Curated Primary Disclosures
          </span>
          <span className="text-[11px] text-gray-400 font-mono">
            {materialList.length} Material Signals
          </span>
        </div>

        {materialList.length === 0 ? (
          <div className="text-center py-8 text-gray-500 text-xs bg-gray-900/50 rounded-2xl border border-gray-800">
            No filings match category filter in this window.
          </div>
        ) : (
          materialList.map(ann => {
            const isHigh = ann.priority === 'HIGH';
            const isResults = ann.category === 'results' && ann.results_enrichment;
            const isMgmt = ann.category === 'management_change' && ann.management_enrichment;

            return (
              <div
                key={ann.id}
                onClick={() => onSelectStockForResearch(ann.ticker)}
                className={`p-4 rounded-2xl border transition-all cursor-pointer shadow-lg active:scale-99 ${
                  isHigh
                    ? 'bg-gray-900/90 border-gray-700/80 hover:border-blue-500/60 shadow-blue-950/10'
                    : 'bg-gray-900/60 border-gray-800 hover:border-gray-700'
                }`}
              >
                {/* Top Bar: Ticker, Category Badge, Priority Indicator */}
                <div className="flex items-center justify-between gap-2 mb-2">
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-sm text-white tracking-wide">
                      {ann.ticker}
                    </span>
                    <span className="text-[10px] text-gray-400 font-normal truncate max-w-[120px]">
                      {ann.company_name}
                    </span>
                  </div>

                  <div className="flex items-center gap-1.5">
                    <span className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full border ${
                      isHigh
                        ? 'bg-rose-950/80 text-rose-300 border-rose-800/60'
                        : 'bg-blue-950/80 text-blue-300 border-blue-800/60'
                    }`}>
                      {ann.category.replace('_', ' ')}
                    </span>
                    {isHigh && (
                      <span className="w-1.5 h-1.5 rounded-full bg-rose-500 animate-pulse"></span>
                    )}
                  </div>
                </div>

                {/* Dense One-Line Summary */}
                <h4 className="text-xs font-semibold text-gray-100 leading-snug">
                  {ann.one_line_summary}
                </h4>

                {/* SHOWCASE ENRICHMENT 1: Quarterly Results Instant First-Cut */}
                {isResults && ann.results_enrichment && (
                  <div className="mt-3 p-3 rounded-xl bg-gray-950 border border-gray-800/90">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-[10px] font-bold text-blue-400 uppercase tracking-wider font-mono">
                        {ann.results_enrichment.quarter} Headline Scorecard
                      </span>
                      <span className="text-[10px] text-emerald-400 font-mono font-medium">
                        OPM {ann.results_enrichment.ebitda.margin_pct}% ({ann.results_enrichment.ebitda.margin_yoy_bps ? `+${ann.results_enrichment.ebitda.margin_yoy_bps} bps` : ''})
                      </span>
                    </div>

                    {/* 4 Core Metrics Grid (Revenue, EBITDA, PBT, PAT) */}
                    <div className="grid grid-cols-2 gap-2 text-xs font-mono">
                      {/* Revenue */}
                      <div className="p-2 rounded-lg bg-gray-900 border border-gray-800/80">
                        <div className="text-[10px] text-gray-400 uppercase">Revenue</div>
                        <div className="font-bold text-white text-sm">
                          ₹{ann.results_enrichment.revenue.val_cr.toLocaleString('en-IN')} Cr
                        </div>
                        <div className="flex items-center gap-1 text-[10px] text-emerald-400 mt-0.5">
                          <ArrowUpRight className="w-3 h-3" />
                          <span>+{ann.results_enrichment.revenue.yoy_pct}% YoY</span>
                          <span className="text-gray-500">|</span>
                          <span className="text-gray-300">+{ann.results_enrichment.revenue.qoq_pct}% QoQ</span>
                        </div>
                      </div>

                      {/* EBITDA */}
                      <div className="p-2 rounded-lg bg-gray-900 border border-gray-800/80">
                        <div className="text-[10px] text-gray-400 uppercase">EBITDA</div>
                        <div className="font-bold text-white text-sm">
                          ₹{ann.results_enrichment.ebitda.val_cr.toLocaleString('en-IN')} Cr
                        </div>
                        <div className="flex items-center gap-1 text-[10px] text-emerald-400 mt-0.5">
                          <ArrowUpRight className="w-3 h-3" />
                          <span>+{ann.results_enrichment.ebitda.yoy_pct}% YoY</span>
                        </div>
                      </div>

                      {/* PBT */}
                      <div className="p-2 rounded-lg bg-gray-900 border border-gray-800/80">
                        <div className="text-[10px] text-gray-400 uppercase">PBT</div>
                        <div className="font-bold text-white text-sm">
                          ₹{ann.results_enrichment.pbt.val_cr.toLocaleString('en-IN')} Cr
                        </div>
                        <div className="flex items-center gap-1 text-[10px] text-emerald-400 mt-0.5">
                          <ArrowUpRight className="w-3 h-3" />
                          <span>+{ann.results_enrichment.pbt.yoy_pct}% YoY</span>
                        </div>
                      </div>

                      {/* PAT */}
                      <div className="p-2 rounded-lg bg-gray-900 border border-gray-800/80">
                        <div className="text-[10px] text-gray-400 uppercase">PAT (Net Profit)</div>
                        <div className="font-bold text-emerald-400 text-sm">
                          ₹{ann.results_enrichment.pat.val_cr.toLocaleString('en-IN')} Cr
                        </div>
                        <div className="flex items-center gap-1 text-[10px] text-emerald-400 mt-0.5">
                          <ArrowUpRight className="w-3 h-3" />
                          <span>+{ann.results_enrichment.pat.yoy_pct}% YoY</span>
                        </div>
                      </div>
                    </div>

                    <p className="text-[11px] text-gray-300 mt-2 italic bg-blue-950/20 p-2 rounded-lg border border-blue-900/30">
                      💡 {ann.results_enrichment.headline_verdict}
                    </p>
                  </div>
                )}

                {/* SHOWCASE ENRICHMENT 2: Management Change Executive Pedigree */}
                {isMgmt && ann.management_enrichment && (
                  <div className="mt-3 p-3.5 rounded-xl bg-gradient-to-br from-indigo-950/40 via-gray-950 to-gray-950 border border-indigo-800/50">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-1.5">
                        <UserCheck className="w-4 h-4 text-indigo-400" />
                        <span className="font-bold text-xs text-white">
                          {ann.management_enrichment.incoming_person}
                        </span>
                      </div>
                      <span className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded bg-indigo-900/60 text-indigo-200">
                        {ann.management_enrichment.new_role}
                      </span>
                    </div>

                    <div className="space-y-1.5 my-2">
                      {ann.management_enrichment.career_profile_bullets.map((bullet, idx) => (
                        <div key={idx} className="flex items-start gap-1.5 text-xs text-gray-300">
                          <span className="text-indigo-400 mt-0.5">•</span>
                          <span>{bullet}</span>
                        </div>
                      ))}
                    </div>

                    <div className="mt-2 pt-2 border-t border-indigo-900/50 text-[11px] text-indigo-200/90 font-medium">
                      <span className="font-bold text-indigo-300">Thesis Impact:</span> {ann.management_enrichment.strategic_implication}
                    </div>
                  </div>
                )}

                {/* Card Footer: Timestamp, Why Should I Care button, Deep Dive hint */}
                <div className="mt-3 pt-2.5 border-t border-gray-800/70 flex items-center justify-between text-[11px]">
                  <span className="text-gray-500 font-mono">
                    {new Date(ann.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} IST
                  </span>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={(e) => toggleWhyCare(ann.id, e)}
                      className="text-blue-400 hover:text-blue-300 font-medium flex items-center gap-1 transition-colors px-2 py-0.5 rounded bg-blue-950/40 border border-blue-900/40"
                    >
                      <Info className="w-3 h-3" />
                      <span>Why Care?</span>
                    </button>

                    <span className="text-gray-400 font-medium flex items-center hover:text-white transition-colors">
                      Deep Dive &rarr;
                    </span>
                  </div>
                </div>

                {/* One-Tap "Why Should I Care?" Micro-Drawer */}
                {expandedWhyCare[ann.id] && (
                  <div className="mt-2.5 p-2.5 rounded-lg bg-blue-950/30 border border-blue-800/40 text-xs text-blue-200 animate-in fade-in duration-150">
                    <span className="font-semibold text-blue-300">Investor Thesis: </span>
                    {ann.category === 'results' && "Confirms earnings visibility; check whether like-for-like volume trajectory aligns with management's stated store growth targets."}
                    {ann.category === 'management_change' && "Leadership transitions at the CEO/CFO level typically herald strategic capital reallocations or margin priority shifts."}
                    {ann.category === 'capex' && "Significant capacity expansion signals high management conviction in structural medium-term demand."}
                    {ann.category === 'credit_rating' && "Rating upgrade directly lowers corporate bond borrowing spreads, expanding net interest margins."}
                    {ann.category === 'litigation' && "Clearance of regulatory scrutiny removes overhang and unblocks pending US generic filing approvals."}
                    {!['results', 'management_change', 'capex', 'credit_rating', 'litigation'].includes(ann.category) && "Material corporate disclosure with potential direct impact on balance sheet leverage or shareholder equity."}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* Routine Paperwork Collapsed Drawer (Tenet: Burying Everything Else Beautifully) */}
      {routineList.length > 0 && (
        <div className="mt-6 rounded-2xl bg-gray-950 border border-gray-800/90 overflow-hidden">
          <button
            onClick={() => setShowRoutineCollapsed(!showRoutineCollapsed)}
            className="w-full px-4 py-3 flex items-center justify-between text-left hover:bg-gray-900/50 transition-colors"
          >
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4 text-gray-500" />
              <span className="text-xs font-medium text-gray-400">
                {routineList.length} Routine Compliance Disclosures Collapsed
              </span>
            </div>
            {showRoutineCollapsed ? (
              <ChevronUp className="w-4 h-4 text-gray-400" />
            ) : (
              <ChevronDown className="w-4 h-4 text-gray-400" />
            )}
          </button>

          {showRoutineCollapsed && (
            <div className="divide-y divide-gray-900 px-4 pb-3 border-t border-gray-900">
              {routineList.map(item => (
                <div key={item.id} className="py-2.5 text-xs">
                  <div className="flex items-center justify-between text-gray-400 font-mono text-[10px] mb-0.5">
                    <span className="font-bold text-gray-300">{item.ticker}</span>
                    <span>{item.category}</span>
                  </div>
                  <p className="text-gray-400 text-xs truncate">{item.headline}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

