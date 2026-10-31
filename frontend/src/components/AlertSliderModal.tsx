import React from 'react';
import { X, Sliders, AlertTriangle, Activity } from 'lucide-react';
import { AlertThresholdConfig } from '../types';

interface AlertSliderModalProps {
  isOpen: boolean;
  onClose: () => void;
  config: AlertThresholdConfig;
  onUpdateConfig: (newConfig: AlertThresholdConfig) => void;
  activeAlertCount: number;
}

export const AlertSliderModal: React.FC<AlertSliderModalProps> = ({
  isOpen,
  onClose,
  config,
  onUpdateConfig,
  activeAlertCount
}) => {
  if (!isOpen) return null;

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onUpdateConfig({
      ...config,
      volume_multiplier_threshold: parseFloat(e.target.value)
    });
  };

  const handlePriceChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onUpdateConfig({
      ...config,
      price_change_pct_threshold: parseFloat(e.target.value)
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
      <div 
        className="w-full max-w-md bg-gray-900 border border-gray-800 rounded-t-2xl sm:rounded-2xl p-5 shadow-2xl safe-bottom text-white animate-in slide-in-from-bottom duration-250"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-gray-800">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-blue-600/20 text-blue-400">
              <Sliders className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-semibold text-sm">Alert Sensitivity Thresholds</h3>
              <p className="text-[11px] text-gray-400">Define what constitutes an "unusual" anomaly</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Live Threshold Impact Badge */}
        <div className="mt-4 p-3 rounded-xl bg-blue-950/40 border border-blue-800/40 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-blue-400 animate-pulse" />
            <span className="text-xs text-blue-200 font-medium">Active Triggers Matching</span>
          </div>
          <span className="px-2 py-0.5 rounded-full bg-blue-600 font-bold text-xs">
            {activeAlertCount} Anomalies
          </span>
        </div>

        {/* Sliders Container */}
        <div className="mt-5 space-y-6">
          {/* Slider 1: Volume Spike */}
          <div>
            <div className="flex justify-between items-center mb-1.5">
              <label className="text-xs font-semibold text-gray-200 flex items-center gap-1.5">
                <span>Trading Volume Spike</span>
              </label>
              <span className="text-xs font-mono font-bold text-blue-400 bg-blue-950/60 px-2 py-0.5 rounded border border-blue-900">
                &gt; {config.volume_multiplier_threshold.toFixed(1)}x 20D Avg
              </span>
            </div>
            <input
              type="range"
              min="1.2"
              max="5.0"
              step="0.1"
              value={config.volume_multiplier_threshold}
              onChange={handleVolumeChange}
              className="w-full h-1.5 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-blue-500"
            />
            <div className="flex justify-between text-[10px] text-gray-500 font-mono mt-1">
              <span>1.2x (Sensitive)</span>
              <span>2.5x (Default)</span>
              <span>5.0x (Extreme)</span>
            </div>
          </div>

          {/* Slider 2: Price Move % */}
          <div>
            <div className="flex justify-between items-center mb-1.5">
              <label className="text-xs font-semibold text-gray-200 flex items-center gap-1.5">
                <span>Daily Price Fluctuation</span>
              </label>
              <span className="text-xs font-mono font-bold text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-900">
                &plusmn;{config.price_change_pct_threshold.toFixed(1)}% in Day
              </span>
            </div>
            <input
              type="range"
              min="1.0"
              max="10.0"
              step="0.5"
              value={config.price_change_pct_threshold}
              onChange={handlePriceChange}
              className="w-full h-1.5 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-emerald-500"
            />
            <div className="flex justify-between text-[10px] text-gray-500 font-mono mt-1">
              <span>±1.0% (Tight)</span>
              <span>±4.0% (Default)</span>
              <span>±10.0% (High Volatility)</span>
            </div>
          </div>

          {/* Institutional note */}
          <div className="p-2.5 rounded-lg bg-gray-950 border border-gray-800 text-[11px] text-gray-400 flex items-start gap-2">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-400 shrink-0 mt-0.5" />
            <span>
              Material filings (Quarterly Results, M&amp;A, CEO/CFO changes, and Regulatory orders) always trigger regardless of price movements.
            </span>
          </div>
        </div>

        {/* Done Button */}
        <button
          onClick={onClose}
          className="w-full mt-6 py-2.5 px-4 rounded-xl bg-blue-600 hover:bg-blue-500 font-medium text-xs text-white shadow-lg shadow-blue-600/30 transition-all active:scale-98"
        >
          Apply Thresholds
        </button>
      </div>
    </div>
  );
};

