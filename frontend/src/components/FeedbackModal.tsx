import React, { useState } from 'react';
import { RotateCw, Check } from 'lucide-react';
import { SentimentLabel } from '../types/analysis';

interface FeedbackSectionProps {
  analysisId: string;
  isSubmitting: boolean;
  successMessage: string | null;
  errorMessage: string | null;
  onSubmit: (label: SentimentLabel, comment?: string) => void;
}

export const FeedbackSection: React.FC<FeedbackSectionProps> = ({
  isSubmitting,
  successMessage,
  errorMessage,
  onSubmit,
}) => {
  const [selectedLabel, setSelectedLabel] = useState<SentimentLabel | null>(null);
  const [comment, setComment] = useState('');
  const [hasSubmitted, setHasSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedLabel) return;
    onSubmit(selectedLabel, comment);
    setHasSubmitted(true);
  };

  const handleReset = () => {
    setSelectedLabel(null);
    setComment('');
    setHasSubmitted(false);
  };

  return (
    <div className="bg-[#0f1420] border border-slate-800 rounded-lg p-4 sm:p-5">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
        <div>
          <h3 className="text-base font-semibold text-white">Model Feedback</h3>
          <p className="text-xs text-slate-400 mt-0.5">Submit ground-truth corrections for model calibration</p>
        </div>
      </div>

      {successMessage && hasSubmitted ? (
        <div className="p-3 bg-emerald-950/40 border border-emerald-800/60 rounded flex items-center justify-between text-xs text-emerald-300">
          <div className="flex items-center gap-2">
            <Check className="w-4 h-4 text-emerald-400" />
            <span>{successMessage}</span>
          </div>
          <button
            onClick={handleReset}
            className="text-slate-300 hover:text-white underline text-[11px]"
          >
            Submit another
          </button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-3 text-xs">
          {errorMessage && (
            <p className="text-rose-400 text-xs">{errorMessage}</p>
          )}

          <div>
            <label className="block text-slate-400 mb-1.5 font-medium">
              Was this overall sentiment analysis correct?
            </label>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => setSelectedLabel('POSITIVE')}
                disabled={isSubmitting}
                className={`px-3 py-1.5 rounded border font-medium transition ${
                  selectedLabel === 'POSITIVE'
                    ? 'border-emerald-500 bg-emerald-950/60 text-emerald-300'
                    : 'border-slate-800 bg-[#090d16] text-slate-300 hover:border-slate-700'
                }`}
              >
                Positive
              </button>
              <button
                type="button"
                onClick={() => setSelectedLabel('NEUTRAL')}
                disabled={isSubmitting}
                className={`px-3 py-1.5 rounded border font-medium transition ${
                  selectedLabel === 'NEUTRAL'
                    ? 'border-amber-500 bg-amber-950/60 text-amber-300'
                    : 'border-slate-800 bg-[#090d16] text-slate-300 hover:border-slate-700'
                }`}
              >
                Neutral
              </button>
              <button
                type="button"
                onClick={() => setSelectedLabel('NEGATIVE')}
                disabled={isSubmitting}
                className={`px-3 py-1.5 rounded border font-medium transition ${
                  selectedLabel === 'NEGATIVE'
                    ? 'border-rose-500 bg-rose-950/60 text-rose-300'
                    : 'border-slate-800 bg-[#090d16] text-slate-300 hover:border-slate-700'
                }`}
              >
                Negative
              </button>
            </div>
          </div>

          <div>
            <input
              type="text"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              disabled={isSubmitting}
              placeholder="Optional notes or context..."
              className="w-full px-3 py-1.5 bg-[#090d16] border border-slate-800 rounded text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
            />
          </div>

          <div className="flex justify-end">
            <button
              type="submit"
              disabled={!selectedLabel || isSubmitting}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium rounded border border-slate-700 text-xs transition disabled:opacity-40"
            >
              {isSubmitting ? (
                <>
                  <RotateCw className="w-3.5 h-3.5 animate-spin" />
                  <span>Submitting...</span>
                </>
              ) : (
                <span>Submit Feedback</span>
              )}
            </button>
          </div>
        </form>
      )}
    </div>
  );
};
