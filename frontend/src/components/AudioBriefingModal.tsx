import React, { useState, useEffect } from 'react';
import { X, Play, Square, Volume2, Sparkles } from 'lucide-react';
import { TriggeredAlert, CorporateAnnouncement } from '../types';

interface AudioBriefingModalProps {
  isOpen: boolean;
  onClose: () => void;
  alerts: TriggeredAlert[];
  announcements: CorporateAnnouncement[];
}

export const AudioBriefingModal: React.FC<AudioBriefingModalProps> = ({
  isOpen,
  onClose,
  alerts,
  announcements
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [briefingText, setBriefingText] = useState('');

  useEffect(() => {
    // Generate institutional spoken script from overnight alerts and high-priority filings
    const lines = [
      "Good morning. Here is your ninety-second FINN portfolio intelligence briefing for Indian markets.",
    ];

    if (alerts.length > 0) {
      lines.push(`We are tracking ${alerts.length} critical market anomalies.`);
      alerts.slice(0, 2).forEach(a => {
        lines.push(`${a.ticker}: ${a.headline}.`);
      });
    }

    const highPriority = announcements.filter(a => a.priority === 'HIGH');
    if (highPriority.length > 0) {
      lines.push("On exchange filings:");
      highPriority.slice(0, 2).forEach(h => {
        lines.push(`${h.company_name} filed ${h.category}. ${h.one_line_summary}`);
      });
    }

    lines.push("All underlying primary documents are verified and ready for deep dive. Have a high-conviction trading session.");
    setBriefingText(lines.join(' '));
  }, [alerts, announcements]);

  useEffect(() => {
    return () => {
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const toggleSpeech = () => {
    if (!window.speechSynthesis) {
      alert("Browser speech synthesis not supported on this device.");
      return;
    }

    if (isPlaying) {
      window.speechSynthesis.cancel();
      setIsPlaying(false);
    } else {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(briefingText);
      utterance.rate = 1.05;
      utterance.pitch = 1.0;
      utterance.onend = () => setIsPlaying(false);
      utterance.onerror = () => setIsPlaying(false);
      window.speechSynthesis.speak(utterance);
      setIsPlaying(true);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
      <div 
        className="w-full max-w-md bg-gray-900 border border-gray-800 rounded-t-2xl sm:rounded-2xl p-5 shadow-2xl safe-bottom text-white animate-in slide-in-from-bottom duration-250"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-gray-800">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-indigo-600/20 text-indigo-400">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-semibold text-sm">FINN 90s Morning Briefing</h3>
              <p className="text-[11px] text-gray-400">Audio overview for your morning commute</p>
            </div>
          </div>
          <button
            onClick={() => {
              if (window.speechSynthesis) window.speechSynthesis.cancel();
              setIsPlaying(false);
              onClose();
            }}
            className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Audio Player Card */}
        <div className="mt-4 p-5 rounded-2xl bg-gradient-to-b from-indigo-950/60 to-gray-950 border border-indigo-800/40 text-center">
          {/* Animated sound waves */}
          <div className="flex items-center justify-center gap-1.5 h-10 mb-4">
            {[40, 70, 90, 60, 100, 50, 80, 45, 95, 65].map((h, idx) => (
              <span
                key={idx}
                className={`w-1 rounded-full bg-indigo-400 transition-all duration-300 ${
                  isPlaying ? 'animate-pulse' : 'opacity-40'
                }`}
                style={{
                  height: isPlaying ? `${h}%` : '20%',
                  animationDelay: `${idx * 0.1}s`
                }}
              />
            ))}
          </div>

          {/* Controls */}
          <button
            onClick={toggleSpeech}
            className={`inline-flex items-center justify-center gap-2 px-6 py-3 rounded-full font-semibold text-sm shadow-xl transition-all active:scale-95 ${
              isPlaying
                ? 'bg-rose-600 hover:bg-rose-500 text-white shadow-rose-600/30'
                : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-indigo-600/30'
            }`}
          >
            {isPlaying ? (
              <>
                <Square className="w-4 h-4 fill-white" />
                <span>Pause Briefing</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4 fill-white" />
                <span>Play 90s Executive Pod</span>
              </>
            )}
          </button>
          <p className="text-[11px] text-indigo-300/80 mt-2 font-mono">
            Generated client-side via native Web Speech synthesis
          </p>
        </div>

        {/* Transcript Card */}
        <div className="mt-4 p-3.5 rounded-xl bg-gray-950 border border-gray-800/80">
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-[11px] font-semibold text-gray-400 uppercase tracking-wider">
              Verbatim Telemetry Script
            </span>
            <Volume2 className="w-3.5 h-3.5 text-gray-500" />
          </div>
          <p className="text-xs text-gray-300 leading-relaxed font-sans max-h-36 overflow-y-auto pr-1">
            "{briefingText}"
          </p>
        </div>
      </div>
    </div>
  );
};

