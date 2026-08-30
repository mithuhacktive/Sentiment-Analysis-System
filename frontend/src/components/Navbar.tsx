import React from 'react';
import { Shield, RefreshCw } from 'lucide-react';
import { HealthResponse } from '../types/analysis';

interface NavbarProps {
  health: HealthResponse | null;
  isConnected: boolean | null;
  isChecking: boolean;
  onRefreshHealth: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  health,
  isConnected,
  isChecking,
  onRefreshHealth,
}) => {
  return (
    <header className="border-b border-slate-800 bg-[#0f1420]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-indigo-600 text-white font-semibold">
            <Shield className="w-4 h-4" />
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-base font-bold text-white tracking-tight">
              SentiGuard
            </span>
            <span className="text-[11px] font-mono text-slate-400">
              v{health?.version || '1.0'}
            </span>
            <span className="hidden md:inline text-xs text-slate-400 border-l border-slate-700 pl-2">
              AI Product Sentiment Intelligence
            </span>
          </div>
        </div>

        {/* Status Indicators */}
        <div className="flex items-center gap-2 sm:gap-3 text-xs">
          {/* Offline/Online Mode Tag */}
          {health?.offline_mode !== undefined && (
            <span className="hidden sm:inline-block px-2 py-0.5 rounded border border-slate-700 bg-slate-800 text-slate-300 text-[11px]">
              {health.offline_mode ? 'Offline Mode' : 'Live Data'}
            </span>
          )}

          {/* Model Status */}
          <div
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded border text-[11px] font-medium ${
              health?.model_loaded
                ? 'border-emerald-900/60 bg-emerald-950/40 text-emerald-300'
                : 'border-amber-900/60 bg-amber-950/40 text-amber-300'
            }`}
          >
            <span
              className={`w-1.5 h-1.5 rounded-full ${
                health?.model_loaded ? 'bg-emerald-400' : 'bg-amber-400'
              }`}
            />
            <span>{health?.model_loaded ? 'Model Ready' : 'Model Degraded'}</span>
          </div>

          {/* Backend Status */}
          <div
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded border text-[11px] font-medium ${
              isConnected === true
                ? 'border-slate-700 bg-slate-800 text-slate-200'
                : isConnected === false
                ? 'border-rose-900/60 bg-rose-950/40 text-rose-300'
                : 'border-slate-800 bg-slate-800 text-slate-400'
            }`}
          >
            <span
              className={`w-1.5 h-1.5 rounded-full ${
                isConnected === true
                  ? 'bg-emerald-400'
                  : isConnected === false
                  ? 'bg-rose-400'
                  : 'bg-slate-400 animate-pulse'
              }`}
            />
            <span>{isConnected === true ? 'Connected' : isConnected === false ? 'Offline' : 'Connecting...'}</span>
          </div>

          {/* Refresh Action */}
          <button
            onClick={onRefreshHealth}
            disabled={isChecking}
            title="Refresh backend status"
            className="p-1.5 rounded text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition disabled:opacity-40"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isChecking ? 'animate-spin text-indigo-400' : ''}`} />
          </button>
        </div>
      </div>
    </header>
  );
};
