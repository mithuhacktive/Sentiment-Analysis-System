import React from 'react';
import { ProductInfo, OverallSentiment } from '../types/analysis';

interface ExecutiveSummaryProps {
  product: ProductInfo | null;
  overall: OverallSentiment | null;
  status: string;
}

export const ExecutiveSummary: React.FC<ExecutiveSummaryProps> = ({
  product,
  overall,
  status,
}) => {
  const sentiment = overall?.label || 'NEUTRAL';
  const confidence = overall ? Math.round(overall.confidence * 1000) / 10 : 0;
  const prodConfidence = product ? Math.round(product.confidence * 100) : 0;

  const sentimentStyles = {
    POSITIVE: {
      label: 'POSITIVE',
      text: 'text-emerald-400',
      bg: 'bg-emerald-950/40 border-emerald-800/60',
      bar: 'bg-emerald-500',
    },
    NEGATIVE: {
      label: 'NEGATIVE',
      text: 'text-rose-400',
      bg: 'bg-rose-950/40 border-rose-800/60',
      bar: 'bg-rose-500',
    },
    NEUTRAL: {
      label: 'NEUTRAL',
      text: 'text-amber-400',
      bg: 'bg-amber-950/40 border-amber-800/60',
      bar: 'bg-amber-500',
    },
  }[sentiment];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {/* Left: Product Info */}
      <div className="bg-[#0f1420] border border-slate-800 rounded-lg p-4 sm:p-5 flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between text-xs text-slate-400 mb-1.5">
            <span className="uppercase tracking-wider font-semibold text-[11px]">Product Details</span>
            <span className="px-2 py-0.5 rounded border border-slate-700 bg-slate-800 text-[11px] text-slate-300">
              {status}
            </span>
          </div>

          <h2 className="text-xl font-bold text-white tracking-tight">
            {product?.name || 'Unknown Product'}
          </h2>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mt-4 text-xs">
            <div className="bg-[#090d16] border border-slate-800 rounded p-2.5">
              <span className="text-slate-400 block text-[11px]">Brand</span>
              <span className="text-slate-200 font-medium truncate block mt-0.5">
                {product?.brand || '—'}
              </span>
            </div>

            <div className="bg-[#090d16] border border-slate-800 rounded p-2.5">
              <span className="text-slate-400 block text-[11px]">Model</span>
              <span className="text-slate-200 font-medium truncate block mt-0.5">
                {product?.model || '—'}
              </span>
            </div>

            <div className="bg-[#090d16] border border-slate-800 rounded p-2.5">
              <span className="text-slate-400 block text-[11px]">Region</span>
              <span className="text-slate-200 font-medium truncate block mt-0.5">
                {product?.region || 'Global'}
              </span>
            </div>

            <div className="bg-[#090d16] border border-slate-800 rounded p-2.5">
              <span className="text-slate-400 block text-[11px]">Resolution</span>
              <span className="text-indigo-300 font-medium truncate block mt-0.5">
                {product?.resolution_status || 'RESOLVED'} ({prodConfidence}%)
              </span>
            </div>
          </div>
        </div>

        {product?.variant && (
          <p className="text-xs text-slate-400 mt-3 pt-2 border-t border-slate-800/80">
            Variant: <span className="text-slate-300">{product.variant}</span>
          </p>
        )}
      </div>

      {/* Right: Overall Sentiment & Confidence */}
      <div className="bg-[#0f1420] border border-slate-800 rounded-lg p-4 sm:p-5 flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between text-xs text-slate-400 mb-2">
            <span className="uppercase tracking-wider font-semibold text-[11px]">Overall Sentiment</span>
            {overall?.calibrated && (
              <span className="text-[11px] text-slate-400 font-mono">
                Calibrated
              </span>
            )}
          </div>

          <div className="flex items-center justify-between gap-4 mt-2">
            <div
              className={`inline-flex items-center px-3 py-1.5 rounded border text-base font-bold tracking-wide ${sentimentStyles.bg} ${sentimentStyles.text}`}
            >
              {sentimentStyles.label}
            </div>
            <div className="text-right">
              <span className="text-2xl font-bold text-white font-mono">
                {confidence}%
              </span>
              <span className="block text-[11px] text-slate-400">Confidence</span>
            </div>
          </div>

          {/* Simple Confidence Bar */}
          <div className="mt-4 space-y-1.5">
            <div className="w-full bg-[#090d16] border border-slate-800 rounded-full h-2 overflow-hidden">
              <div
                className={`h-full rounded-full transition-all duration-500 ${sentimentStyles.bar}`}
                style={{ width: `${confidence}%` }}
              />
            </div>
            <div className="flex justify-between text-[10px] text-slate-400">
              <span>0%</span>
              <span>50%</span>
              <span>100%</span>
            </div>
          </div>
        </div>

        <p className="text-xs text-slate-400 mt-3 pt-2 border-t border-slate-800/80">
          Aggregated across deduplicated review signals.
        </p>
      </div>
    </div>
  );
};
