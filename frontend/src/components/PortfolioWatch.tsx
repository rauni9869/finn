import React, { useState, useEffect } from 'react';
import { StockInfo } from '../types';

interface PortfolioWatchProps {
  onSelectStock: (ticker: string) => void;
}

export const PortfolioWatch: React.FC<PortfolioWatchProps> = ({ onSelectStock }) => {
  const [stocks, setStocks] = useState<StockInfo[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [filterSector, setFilterSector] = useState<string>('ALL');
  const [filterAnomalyOnly, setFilterAnomalyOnly] = useState<boolean>(false);

  useEffect(() => {
    fetchPortfolio();
  }, []);

  const fetchPortfolio = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch('/api/portfolio');
      if (!res.ok) {
        throw new Error(`Failed to load portfolio (HTTP ${res.status})`);
      }
      const data: StockInfo[] = await res.json();
      setStocks(data);
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Error connecting to portfolio service');
    } finally {
      setLoading(false);
    }
  };

  const sectors = ['ALL', ...Array.from(new Set(stocks.map((s) => s.sector)))];

  const filteredStocks = stocks.filter((stock) => {
    const matchesSector = filterSector === 'ALL' || stock.sector === filterSector;
    const isAnomaly =
      (stock.eod && (stock.eod.is_unusual_volume || stock.eod.is_unusual_price)) || false;
    const matchesAnomaly = !filterAnomalyOnly || isAnomaly;
    return matchesSector && matchesAnomaly;
  });

  return (
    <div className="space-y-4 pb-20">
      {/* Portfolio Header Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 sm:p-5 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-base font-bold text-slate-100 flex items-center gap-2">
              <span>Investment Universe</span>
              <span className="text-xs bg-slate-800 border border-slate-700 text-slate-300 font-mono px-2 py-0.5 rounded">
                18 Core Holdings + Ad-hoc Universe
              </span>
            </h2>
            <p className="text-xs text-slate-400 mt-1">
              End-of-day price action, 20-day volume multiples, and one-tap research launching.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setFilterAnomalyOnly(!filterAnomalyOnly)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors border flex items-center gap-1.5 ${
                filterAnomalyOnly
                  ? 'bg-amber-500/20 text-amber-300 border-amber-500/40 font-semibold'
                  : 'bg-slate-800 text-slate-400 border-slate-700 hover:text-slate-200'
              }`}
            >
              <span>⚡ Anomaly Alerts Only</span>
            </button>
            <button
              onClick={fetchPortfolio}
              className="p-1.5 bg-slate-800 hover:bg-slate-750 text-slate-300 rounded-lg text-xs border border-slate-700 transition-colors"
              title="Refresh universe"
            >
              🔄
            </button>
          </div>
        </div>

        {/* Sector Filter Chips */}
        <div className="flex gap-1.5 overflow-x-auto pt-4 pb-1 scrollbar-thin">
          {sectors.map((sector) => (
            <button
              key={sector}
              onClick={() => setFilterSector(sector)}
              className={`px-2.5 py-1 rounded-md text-xs font-medium whitespace-nowrap transition-colors ${
                filterSector === sector
                  ? 'bg-emerald-600 text-white font-semibold shadow-sm'
                  : 'bg-slate-800 text-slate-400 hover:text-slate-200'
              }`}
            >
              {sector}
            </button>
          ))}
        </div>
      </div>

      {/* Loading Skeleton */}
      {loading && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 text-center space-y-3">
          <div className="inline-block animate-spin h-7 w-7 border-2 border-emerald-500 border-t-transparent rounded-full"></div>
          <p className="text-xs text-slate-400">Loading portfolio universe and EOD metrics...</p>
        </div>
      )}

      {/* Error View */}
      {error && !loading && (
        <div className="bg-rose-950/40 border border-rose-800/50 rounded-xl p-5 text-center space-y-2">
          <div className="text-rose-400 text-sm font-semibold">Unable to fetch portfolio</div>
          <p className="text-xs text-slate-400">{error}</p>
          <button
            onClick={fetchPortfolio}
            className="px-3 py-1 bg-rose-600 hover:bg-rose-500 text-white rounded text-xs"
          >
            Retry
          </button>
        </div>
      )}

      {/* Stocks Table / Card List */}
      {!loading && !error && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-slate-800 bg-slate-950/50 text-slate-400 font-medium">
                  <th className="py-3 px-4">Ticker / Company</th>
                  <th className="py-3 px-3">Sector</th>
                  <th className="py-3 px-3 text-right">EOD Close</th>
                  <th className="py-3 px-3 text-right">Day Change</th>
                  <th className="py-3 px-3 text-right">Volume / 20d Avg</th>
                  <th className="py-3 px-4 text-center">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-sans">
                {filteredStocks.map((stock) => {
                  const eod = stock.eod;
                  const isPositive = (eod?.pct_change || 0) >= 0;
                  const volMultiple = eod?.volume_multiple || 1.0;
                  const isVolumeSpike = volMultiple >= 2.0;

                  return (
                    <tr
                      key={stock.ticker}
                      className="hover:bg-slate-850/50 transition-colors cursor-pointer group"
                      onClick={() => onSelectStock(stock.ticker)}
                    >
                      {/* Ticker & Name */}
                      <td className="py-3.5 px-4 align-middle">
                        <div className="flex items-center gap-2">
                          <span className="font-mono font-bold text-slate-100 text-sm group-hover:text-emerald-400 transition-colors">
                            {stock.ticker}
                          </span>
                          {!stock.is_portfolio && (
                            <span className="text-[10px] font-mono px-1.5 py-0.2 bg-purple-500/20 text-purple-300 border border-purple-500/30 rounded">
                              Ad-hoc
                            </span>
                          )}
                          {eod?.is_unusual_volume && (
                            <span className="text-[10px] font-bold px-1.5 py-0.2 bg-amber-500/20 text-amber-300 border border-amber-500/30 rounded">
                              ⚡ Vol {volMultiple.toFixed(1)}x
                            </span>
                          )}
                          {eod?.is_unusual_price && (
                            <span className="text-[10px] font-bold px-1.5 py-0.2 bg-rose-500/20 text-rose-300 border border-rose-500/30 rounded">
                              Move {eod.pct_change.toFixed(1)}%
                            </span>
                          )}
                        </div>
                        <div className="text-[11px] text-slate-400 truncate max-w-[200px] mt-0.5">
                          {stock.name}
                        </div>
                      </td>

                      {/* Sector */}
                      <td className="py-3.5 px-3 text-slate-400 align-middle">
                        <span className="bg-slate-950 px-2 py-1 rounded text-[11px] border border-slate-800">
                          {stock.sector}
                        </span>
                      </td>

                      {/* EOD Price */}
                      <td className="py-3.5 px-3 text-right font-mono font-bold text-slate-200 align-middle">
                        ₹{eod?.close ? eod.close.toLocaleString() : '—'}
                      </td>

                      {/* Day Change */}
                      <td className="py-3.5 px-3 text-right font-mono align-middle">
                        {eod ? (
                          <span
                            className={`inline-block font-semibold px-1.5 py-0.5 rounded text-xs ${
                              isPositive
                                ? 'bg-emerald-500/10 text-emerald-400'
                                : 'bg-rose-500/10 text-rose-400'
                            }`}
                          >
                            {isPositive ? '+' : ''}
                            {eod.pct_change.toFixed(2)}%
                          </span>
                        ) : (
                          '—'
                        )}
                      </td>

                      {/* Volume multiple */}
                      <td className="py-3.5 px-3 text-right font-mono align-middle">
                        <span
                          className={`font-semibold text-xs ${
                            isVolumeSpike ? 'text-amber-400 font-bold' : 'text-slate-400'
                          }`}
                        >
                          {volMultiple.toFixed(2)}x
                        </span>
                        <div className="text-[10px] text-slate-500">
                          {eod ? (eod.volume / 100000).toFixed(1) + 'L shares' : ''}
                        </div>
                      </td>

                      {/* Action */}
                      <td className="py-3.5 px-4 text-center align-middle">
                        <button
                          type="button"
                          onClick={(e) => {
                            e.stopPropagation();
                            onSelectStock(stock.ticker);
                          }}
                          className="px-2.5 py-1 bg-slate-800 hover:bg-emerald-600 hover:text-white text-slate-300 text-xs font-medium rounded-md transition-all border border-slate-700 hover:border-emerald-500"
                        >
                          Research ›
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

