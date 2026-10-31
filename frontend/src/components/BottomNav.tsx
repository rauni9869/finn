import React from 'react';

interface BottomNavProps {
  activeTab: 'push' | 'pull' | 'portfolio';
  onChangeTab: (tab: 'push' | 'pull' | 'portfolio') => void;
  unreadCount?: number;
}

export const BottomNav: React.FC<BottomNavProps> = ({
  activeTab,
  onChangeTab,
  unreadCount = 0,
}) => {
  return (
    <div className="fixed bottom-0 left-0 right-0 z-40 bg-slate-900/95 backdrop-blur-md border-t border-slate-800 px-4 py-2 sm:hidden">
      <div className="flex items-center justify-around max-w-md mx-auto">
        {/* Push Digest Feed */}
        <button
          onClick={() => onChangeTab('push')}
          className={`relative flex flex-col items-center gap-1 py-1 px-3 rounded-lg transition-colors ${
            activeTab === 'push'
              ? 'text-emerald-400 font-semibold'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <span className="text-lg">⚡</span>
          <span className="text-[11px]">Push Feed</span>
          {unreadCount > 0 && (
            <span className="absolute top-0 right-2 h-4 w-4 rounded-full bg-rose-500 text-white text-[9px] font-mono font-bold flex items-center justify-center">
              {unreadCount > 9 ? '9+' : unreadCount}
            </span>
          )}
        </button>

        {/* Pull Research Hub */}
        <button
          onClick={() => onChangeTab('pull')}
          className={`flex flex-col items-center gap-1 py-1 px-3 rounded-lg transition-colors ${
            activeTab === 'pull'
              ? 'text-emerald-400 font-semibold'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <span className="text-lg">⚖</span>
          <span className="text-[11px]">Pull Research</span>
        </button>

        {/* Portfolio Watch */}
        <button
          onClick={() => onChangeTab('portfolio')}
          className={`flex flex-col items-center gap-1 py-1 px-3 rounded-lg transition-colors ${
            activeTab === 'portfolio'
              ? 'text-emerald-400 font-semibold'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <span className="text-lg">📊</span>
          <span className="text-[11px]">Universe</span>
        </button>
      </div>
    </div>
  );
};

