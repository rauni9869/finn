import React, { useState, useEffect, useRef } from 'react';
import { API_BASE } from './api';
import { Header } from './components/Header';
import { PushDigestFeed } from './components/PushDigestFeed';
import { PullResearchHub } from './components/PullResearchHub';
import { PortfolioWatch } from './components/PortfolioWatch';
import { BottomNav } from './components/BottomNav';
import { AlertSliderModal } from './components/AlertSliderModal';
import { AudioBriefingModal } from './components/AudioBriefingModal';
import { 
  CorporateAnnouncement, 
  TriggeredAlert, 
  AlertThresholdConfig,
  WindowedDigestResponse 
} from './types';

export const App: React.FC = () => {
  // Navigation State
  const [activeTab, setActiveTab] = useState<'push' | 'pull' | 'portfolio'>('push');
  const [selectedResearchTicker, setSelectedResearchTicker] = useState<string>('TRENT');

  // Push Data State
  const [windowHours, setWindowHours] = useState<number>(24);
  const [announcements, setAnnouncements] = useState<CorporateAnnouncement[]>([]);
  const [alerts, setAlerts] = useState<TriggeredAlert[]>([]);
  const [portfolioCount, setPortfolioCount] = useState<number>(18);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [dataAsOf, setDataAsOf] = useState<string | null>(null);
  const latestAlertRequest = useRef(0);

  // Modals
  const [isAlertModalOpen, setIsAlertModalOpen] = useState<boolean>(false);
  const [isAudioModalOpen, setIsAudioModalOpen] = useState<boolean>(false);

  // Alert Config
  const [alertConfig, setAlertConfig] = useState<AlertThresholdConfig>({
    volume_multiplier_threshold: 2.0,
    price_change_pct_threshold: 4.0,
    material_categories: ['results', 'M&A', 'fund_raise', 'management_change'],
  });

  // Fetch Push Digest
  const fetchDigest = async (hours: number) => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams({
        window_hours: String(hours),
        vol_thresh: String(alertConfig.volume_multiplier_threshold),
        price_thresh: String(alertConfig.price_change_pct_threshold),
      });
      const res = await fetch(`${API_BASE}/api/digest?${params}`);
      if (!res.ok) {
        throw new Error(`Failed to fetch digest (HTTP ${res.status})`);
      }
      const data: WindowedDigestResponse = await res.json();
      setAnnouncements(data.announcements);
      setAlerts(data.active_alerts);
      setDataAsOf(data.is_sample_data ? data.data_as_of ?? null : null);
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Error connecting to backend API');
    } finally {
      setLoading(false);
    }
  };

  // Fetch Portfolio Count
  const fetchPortfolioMetadata = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/portfolio`);
      if (res.ok) {
        const data = await res.json();
        setPortfolioCount(data.length);
      }
    } catch (err) {
      console.warn('Could not load portfolio list for count', err);
    }
  };

  useEffect(() => {
    fetchDigest(windowHours);
    fetchPortfolioMetadata();
  }, [windowHours]);

  // Handle changing alert configuration
  const handleUpdateConfig = async (newConfig: AlertThresholdConfig) => {
    setAlertConfig(newConfig);
    const requestId = ++latestAlertRequest.current;
    try {
      const res = await fetch(`${API_BASE}/api/alerts/evaluate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newConfig),
      });
      if (!res.ok) {
        throw new Error(`Failed to evaluate alerts (HTTP ${res.status})`);
      }
      const updatedAlerts: TriggeredAlert[] = await res.json();
      // Sliders fire quickly, so ignore any response that isn't for the latest position
      if (requestId === latestAlertRequest.current) {
        setAlerts(updatedAlerts);
      }
    } catch (err) {
      console.error('Failed to evaluate alert thresholds', err);
    }
  };

  // Transition from Push Feed or Portfolio Watch directly into Deep Pull Research
  const handleSelectStockForResearch = (ticker: string) => {
    setSelectedResearchTicker(ticker);
    setActiveTab('pull');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans antialiased selection:bg-emerald-500/30 selection:text-emerald-200">
      {/* Header */}
      <Header
        portfolioCount={portfolioCount}
        alerts={alerts}
        onOpenAlertModal={() => setIsAlertModalOpen(true)}
        onOpenAudioBriefing={() => setIsAudioModalOpen(true)}
        onViewAlerts={() => {
          setActiveTab('push');
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }}
      />

      {/* Desktop / Tablet Sub-Header Tab Bar */}
      <div className="hidden sm:block border-b border-slate-800/80 bg-slate-900/60 sticky top-14 z-30 backdrop-blur-md">
        <div className="max-w-4xl mx-auto px-4 flex items-center justify-between">
          <div className="flex gap-1 py-2">
            <button
              onClick={() => setActiveTab('push')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ${
                activeTab === 'push'
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <span>⚡ Push Digest Feed</span>
              {alerts.length > 0 && (
                <span className="h-4 px-1.5 rounded-full bg-rose-500/20 text-rose-300 font-mono text-[10px] border border-rose-500/30 flex items-center justify-center">
                  {alerts.length}
                </span>
              )}
            </button>

            <button
              onClick={() => setActiveTab('pull')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ${
                activeTab === 'pull'
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <span>⚖ Pull Research Hub</span>
              <span className="text-[10px] font-mono text-slate-500">
                ({selectedResearchTicker})
              </span>
            </button>

            <button
              onClick={() => setActiveTab('portfolio')}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all flex items-center gap-1.5 ${
                activeTab === 'portfolio'
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <span>📊 Investment Universe</span>
              <span className="text-[10px] font-mono text-slate-500">({portfolioCount})</span>
            </button>
          </div>

          <div className="flex items-center gap-2 text-xs text-slate-400">
            <button
              onClick={() => fetchDigest(windowHours)}
              className="p-1 text-slate-400 hover:text-slate-200 transition-colors"
              title="Refresh live feed"
            >
              🔄
            </button>
          </div>
        </div>
      </div>

      {/* Main Body */}
      <main className="flex-1 max-w-4xl w-full mx-auto p-3 sm:p-5">
        {/* Error Notification */}
        {error && (
          <div className="mb-4 p-3 bg-rose-950/40 border border-rose-800/60 rounded-xl text-xs text-rose-300 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span>⚠</span>
              <span>{error}</span>
            </div>
            <button
              onClick={() => fetchDigest(windowHours)}
              className="px-2 py-0.5 bg-rose-900/60 hover:bg-rose-800 rounded font-semibold text-[11px]"
            >
              Retry
            </button>
          </div>
        )}

        {/* Tab 1: Push Digest Feed */}
        {activeTab === 'push' && loading && announcements.length === 0 && (
          <div className="mb-4 p-6 text-center text-xs text-slate-400 bg-slate-900 border border-slate-800 rounded-xl">
            Loading filings and end-of-day market data. The first load can take about 30 seconds...
          </div>
        )}
        {activeTab === 'push' && dataAsOf && (
          <div className="mb-3 px-3 py-2 text-[11px] text-amber-200/90 bg-amber-950/30 border border-amber-800/40 rounded-lg">
            Filings are sample data, with the window measured back from {new Date(dataAsOf).toLocaleDateString()}. Prices and alerts are live end-of-day data.
          </div>
        )}
        {activeTab === 'push' && (
          <PushDigestFeed
            announcements={announcements}
            alerts={alerts}
            windowHours={windowHours}
            onSelectWindow={(hours) => setWindowHours(hours)}
            onSelectStockForResearch={handleSelectStockForResearch}
          />
        )}

        {/* Tab 2: Pull Research Hub */}
        {activeTab === 'pull' && (
          <PullResearchHub
            initialTicker={selectedResearchTicker}
            onSelectTicker={(ticker) => setSelectedResearchTicker(ticker)}
          />
        )}

        {/* Tab 3: Portfolio Watch */}
        {activeTab === 'portfolio' && (
          <PortfolioWatch onSelectStock={handleSelectStockForResearch} />
        )}
      </main>

      {/* Mobile Bottom Navigation */}
      <BottomNav
        activeTab={activeTab}
        onChangeTab={(tab) => {
          setActiveTab(tab);
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }}
        unreadCount={alerts.length}
      />

      {/* Threshold Configuration Slider Modal */}
      <AlertSliderModal
        isOpen={isAlertModalOpen}
        onClose={() => setIsAlertModalOpen(false)}
        config={alertConfig}
        onUpdateConfig={handleUpdateConfig}
        activeAlertCount={alerts.length}
      />

      {/* 90-Second Morning Audio Pod Briefing Modal */}
      <AudioBriefingModal
        isOpen={isAudioModalOpen}
        onClose={() => setIsAudioModalOpen(false)}
        alerts={alerts}
        announcements={announcements}
      />
    </div>
  );
};

export default App;

