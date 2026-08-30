import React from 'react';
import { RotateCw } from 'lucide-react';

interface LoadingStateProps {
  currentStage: string;
}

export const LoadingState: React.FC<LoadingStateProps> = ({ currentStage }) => {
  return (
    <div className="w-full bg-[#0f1420] border border-slate-800 rounded-lg p-8 sm:p-12 text-center space-y-4">
      <div className="inline-flex items-center justify-center w-10 h-10 rounded-lg bg-indigo-950/60 border border-indigo-800/60 text-indigo-400">
        <RotateCw className="w-5 h-5 animate-spin" />
      </div>

      <div className="space-y-1">
        <h3 className="text-base font-semibold text-white">
          {currentStage || 'Analyzing product sentiment...'}
        </h3>
        <p className="text-xs text-slate-400 max-w-sm mx-auto">
          Retrieving multi-source reviews, filtering duplicates, scoring evidence quality, and computing aspect sentiments.
        </p>
      </div>

      {/* Subtle Step Bar */}
      <div className="flex justify-center gap-2 pt-2 text-[11px] text-slate-400">
        <span className="px-2 py-0.5 rounded bg-[#090d16] border border-slate-800">
          Entity Resolution
        </span>
        <span className="px-2 py-0.5 rounded bg-[#090d16] border border-slate-800">
          Review Retrieval
        </span>
        <span className="px-2 py-0.5 rounded bg-[#090d16] border border-slate-800">
          RoBERTa Inference
        </span>
        <span className="px-2 py-0.5 rounded bg-[#090d16] border border-slate-800">
          Aggregation
        </span>
      </div>
    </div>
  );
};
