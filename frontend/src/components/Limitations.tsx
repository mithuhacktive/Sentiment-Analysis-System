import React from 'react';
import { Info, CheckCircle2 } from 'lucide-react';

interface LimitationsProps {
  limitations: string[];
}

export const Limitations: React.FC<LimitationsProps> = ({ limitations }) => {
  const hasLimitations = limitations && limitations.length > 0;

  return (
    <div className="bg-[#0f1420] border border-slate-800 rounded-lg p-4 sm:p-5">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
        <h3 className="text-base font-semibold text-white">
          Limitations & Diagnostics
        </h3>
        <span className="text-xs text-slate-400">
          {hasLimitations ? `${limitations.length} notice(s)` : 'Clear'}
        </span>
      </div>

      {hasLimitations ? (
        <div className="space-y-2 text-xs">
          {limitations.map((lim, idx) => (
            <div
              key={idx}
              className="flex items-start gap-2.5 p-2.5 rounded bg-slate-900 border border-slate-800 text-slate-300"
            >
              <Info className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
              <span>{lim}</span>
            </div>
          ))}
        </div>
      ) : (
        <div className="flex items-center gap-2 text-xs text-slate-400">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>No known pipeline limitations reported for this analysis.</span>
        </div>
      )}
    </div>
  );
};
