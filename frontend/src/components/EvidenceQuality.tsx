import React from 'react';
import { EvidenceSummary } from '../types/analysis';

interface EvidenceQualityProps {
  evidence: EvidenceSummary | null;
}

export const EvidenceQuality: React.FC<EvidenceQualityProps> = ({ evidence }) => {
  if (!evidence) {
    return (
      <div className="bg-[#0f1420] border border-slate-800 rounded-lg p-4 sm:p-5">
        <h3 className="text-sm font-semibold text-white uppercase tracking-wider text-[11px] text-slate-400 mb-2">
          Evidence Quality
        </h3>
        <p className="text-slate-400 text-xs">No evidence metrics available.</p>
      </div>
    );
  }

  const conflict = (evidence.conflict_level || 'LOW').toUpperCase();

  const conflictStyle = {
    LOW: 'text-emerald-400 border-emerald-800/60 bg-emerald-950/40',
    MEDIUM: 'text-amber-400 border-amber-800/60 bg-amber-950/40',
    HIGH: 'text-rose-400 border-rose-800/60 bg-rose-950/40',
  }[conflict] || 'text-slate-300 border-slate-700 bg-slate-800';

  const metrics = [
    { label: 'Reviews Analyzed', value: evidence.reviews_analyzed, sub: 'Total parsed' },
    { label: 'Independent Reviews', value: evidence.independent_reviews, sub: 'Deduplicated' },
    { label: 'Sources', value: evidence.sources, sub: 'Active channels' },
    { label: 'Duplicates', value: evidence.duplicates, sub: 'Filtered' },
    { label: 'Suspicious Reviews', value: evidence.suspicious_reviews, sub: 'Spam/bot flags' },
  ];

  return (
    <div className="bg-[#0f1420] border border-slate-800 rounded-lg p-4 sm:p-5 space-y-3">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div>
          <h3 className="text-base font-semibold text-white">Evidence & Quality</h3>
          <p className="text-xs text-slate-400 mt-0.5">Corpus integrity and consensus breakdown</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400">Conflict Level:</span>
          <span className={`px-2 py-0.5 rounded border text-xs font-semibold ${conflictStyle}`}>
            {conflict}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
        {metrics.map((m, idx) => (
          <div key={idx} className="bg-[#090d16] border border-slate-800 rounded p-3">
            <span className="text-[11px] text-slate-400 block truncate">{m.label}</span>
            <span className="text-xl font-bold text-white font-mono block mt-1">
              {m.value}
            </span>
            <span className="text-[10px] text-slate-400 block mt-0.5">{m.sub}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
