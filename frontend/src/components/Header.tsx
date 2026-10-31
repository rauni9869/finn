import React from 'react';
import { Sliders, Bell, Volume2, Shield } from 'lucide-react';
import { TriggeredAlert } from '../types';

interface HeaderProps {
  portfolioCount: number;
  alerts: TriggeredAlert[];
  onOpenAlertModal: () => void;
  onOpenAudioBriefing: () => void;
  onViewAlerts: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  portfolioCount,
  alerts,
  onOpenAlertModal,
  onOpenAudioBriefing,
  onViewAlerts
}) => {
  return (
    <header className="sticky top-0 z-40 bg-[#0B0F19]/95 backdrop-blur-md border-b border-gray-800/80 px-4 py-3">
      <div className="max-w-md mx-auto flex items-center justify-between">
        {/* Brand & Market Status */}
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/20">
            F
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <h1 className="font-bold text-base tracking-tight text-white">FINN</h1>
              <span className="text-[10px] uppercase font-semibold px-1.5 py-0.5 rounded bg-blue-950 text-blue-400 border border-blue-800/60">
                NSE/BSE
              </span>
            </div>
            <div className="flex items-center gap-1.5 text-xs text-gray-400">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="font-medium text-[11px] text-gray-300">{portfolioCount} Stocks Monitored</span>
            </div>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2">
          {/* 90s Audio Morning Pod Button */}
          <button
            onClick={onOpenAudioBriefing}
            className="flex items-center gap-1 text-xs font-medium px-2.5 py-1.5 rounded-lg bg-indigo-950/80 hover:bg-indigo-900 border border-indigo-700/50 text-indigo-300 transition-all active:scale-95"
            title="90-Second Morning Audio Briefing"
          >
            <Volume2 className="w-3.5 h-3.5 text-indigo-400" />
            <span className="hidden sm:inline">Briefing</span>
          </button>

          {/* Alert Trigger Bell */}
          <button
            onClick={onViewAlerts}
            className="relative p-2 rounded-lg bg-gray-900 hover:bg-gray-800 border border-gray-800 text-gray-300 transition-all active:scale-95"
            title="Active Triggered Alerts"
          >
            <Bell className="w-4 h-4" />
            {alerts.length > 0 && (
              <span className="absolute -top-1 -right-1 px-1.5 py-0.2 min-w-4.5 h-4.5 rounded-full bg-rose-600 text-white text-[10px] font-bold flex items-center justify-center ring-2 ring-[#0B0F19]">
                {alerts.length}
              </span>
            )}
          </button>

          {/* Configurable Threshold Sliders Trigger */}
          <button
            onClick={onOpenAlertModal}
            className="p-2 rounded-lg bg-gray-900 hover:bg-gray-800 border border-gray-800 text-gray-300 transition-all active:scale-95"
            title="Threshold Sliders"
          >
            <Sliders className="w-4 h-4 text-gray-300" />
          </button>
        </div>
      </div>
    </header>
  );
};

