import React from 'react';
import { AlertCircle, RotateCcw } from 'lucide-react';
import { ApiError } from '../types/analysis';

interface ErrorStateProps {
  error: ApiError | null;
  onRetry?: () => void;
  onReset: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  error,
  onRetry,
  onReset,
}) => {
  if (!error) return null;

  return (
    <div className="bg-[#0f1420] border border-rose-800/60 rounded-lg p-5 sm:p-6 space-y-4">
      <div className="flex items-start gap-3">
        <AlertCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
        <div className="space-y-1 flex-1">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-rose-400 uppercase tracking-wider">
              {error.status ? `Error ${error.status}` : 'Request Error'}
            </span>
          </div>
          <p className="text-sm font-medium text-slate-200">
            {error.message}
          </p>

          {error.detail && typeof error.detail === 'object' && (
            <pre className="mt-2 p-2 bg-[#090d16] rounded border border-slate-800 text-[11px] font-mono text-slate-400 overflow-x-auto">
              {JSON.stringify(error.detail, null, 2)}
            </pre>
          )}
        </div>
      </div>

      <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-800/80 text-xs">
        <button
          onClick={onReset}
          className="px-3 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 transition"
        >
          Dismiss
        </button>

        {onRetry && (
          <button
            onClick={onRetry}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded bg-rose-900/60 hover:bg-rose-800/60 text-rose-200 border border-rose-700/60 transition"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Retry</span>
          </button>
        )}
      </div>
    </div>
  );
};
