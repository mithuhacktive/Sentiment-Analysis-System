import React from 'react';
import { PipelineInfo as PipelineInfoType } from '../types/analysis';

interface PipelineInfoProps {
  pipeline: PipelineInfoType | null;
  analysisId?: string;
}

export const PipelineInfo: React.FC<PipelineInfoProps> = ({
  pipeline,
  analysisId,
}) => {
  if (!pipeline) return null;

  const formattedTime = new Date(pipeline.retrieved_at).toLocaleString();

  return (
    <div className="bg-[#0f1420] border border-slate-800 rounded-lg p-4 sm:p-5">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
        <h3 className="text-base font-semibold text-white">Pipeline Telemetry</h3>
        {analysisId && (
          <span className="text-[11px] font-mono text-slate-400">
            ID: <span className="text-slate-300">{analysisId}</span>
          </span>
        )}
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 text-xs">
        <div className="bg-[#090d16] border border-slate-800 rounded p-2.5">
          <span className="text-slate-400 block text-[11px]">Model</span>
          <span className="text-slate-200 font-mono font-medium truncate block mt-0.5" title={pipeline.model}>
            {pipeline.model}
          </span>
        </div>

        <div className="bg-[#090d16] border border-slate-800 rounded p-2.5">
          <span className="text-slate-400 block text-[11px]">Processing Time</span>
          <span className="text-slate-200 font-mono font-medium block mt-0.5">
            {pipeline.processing_time_ms.toFixed(1)} ms
          </span>
        </div>

        <div className="bg-[#090d16] border border-slate-800 rounded p-2.5">
          <span className="text-slate-400 block text-[11px]">Data Freshness</span>
          <span className="text-slate-200 font-medium block mt-0.5">
            {pipeline.data_freshness}
          </span>
        </div>

        <div className="bg-[#090d16] border border-slate-800 rounded p-2.5">
          <span className="text-slate-400 block text-[11px]">Cache Status</span>
          <span className="text-slate-200 font-medium block mt-0.5">
            {pipeline.cache_used ? 'Cache Hit' : 'Live Execution'}
          </span>
        </div>

        <div className="bg-[#090d16] border border-slate-800 rounded p-2.5">
          <span className="text-slate-400 block text-[11px]">Timestamp</span>
          <span className="text-slate-200 font-medium truncate block mt-0.5" title={pipeline.retrieved_at}>
            {formattedTime}
          </span>
        </div>
      </div>
    </div>
  );
};
