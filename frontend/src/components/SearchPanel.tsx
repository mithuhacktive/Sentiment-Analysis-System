import React, { useState } from 'react';
import { Search, RotateCw } from 'lucide-react';
import { AnalyzeRequest } from '../types/analysis';

interface SearchPanelProps {
  isLoading: boolean;
  onAnalyze: (request: AnalyzeRequest) => void;
  initialQuery?: string;
}

const POPULAR_QUERIES = [
  'Sony WH-1000XM5',
  'Apple iPhone 15 Pro',
  'MacBook Air M3',
  'Bose QuietComfort Ultra',
];

const REGIONS = [
  { value: '', label: 'Global / All' },
  { value: 'US', label: 'US' },
  { value: 'UK', label: 'UK' },
  { value: 'IN', label: 'IN' },
  { value: 'EU', label: 'EU' },
  { value: 'CA', label: 'CA' },
];

const REVIEW_LIMITS = [10, 25, 50, 100];

export const SearchPanel: React.FC<SearchPanelProps> = ({
  isLoading,
  onAnalyze,
  initialQuery = '',
}) => {
  const [query, setQuery] = useState(initialQuery);
  const [region, setRegion] = useState('');
  const [maxReviews, setMaxReviews] = useState<number>(25);
  const [fresh, setFresh] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const clean = query.trim();
    if (!clean) {
      setValidationError('Please enter a product name or URL.');
      return;
    }
    setValidationError(null);
    onAnalyze({
      query: clean,
      fresh,
      region: region || null,
      max_reviews: maxReviews || null,
    });
  };

  const handleSelectPreset = (preset: string) => {
    setQuery(preset);
    setValidationError(null);
    onAnalyze({
      query: preset,
      fresh,
      region: region || null,
      max_reviews: maxReviews || null,
    });
  };

  return (
    <div className="bg-[#0f1420] border border-slate-800 rounded-lg p-4 sm:p-5">
      <form onSubmit={handleSubmit} className="space-y-3">
        {/* Main Search Row */}
        <div className="flex gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" />
            <input
              type="text"
              value={query}
              onChange={(e) => {
                setQuery(e.target.value);
                if (validationError) setValidationError(null);
              }}
              disabled={isLoading}
              placeholder="Enter a product name, keyword, or product URL (e.g. Sony WH-1000XM5)..."
              className="w-full pl-9 pr-3 py-2 bg-[#090d16] border border-slate-700 rounded-md text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition disabled:opacity-50"
            />
          </div>
          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className="inline-flex items-center justify-center gap-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 active:bg-indigo-700 text-white text-sm font-medium rounded-md transition disabled:opacity-40 disabled:pointer-events-none shrink-0"
          >
            {isLoading ? (
              <>
                <RotateCw className="w-3.5 h-3.5 animate-spin" />
                <span>Analyzing</span>
              </>
            ) : (
              <span>Analyze</span>
            )}
          </button>
        </div>

        {validationError && (
          <p className="text-xs text-rose-400 font-medium">{validationError}</p>
        )}

        {/* Options Row */}
        <div className="flex flex-wrap items-center justify-between gap-3 pt-1 border-t border-slate-800/80 text-xs text-slate-400">
          <div className="flex flex-wrap items-center gap-4">
            {/* Region */}
            <div className="flex items-center gap-1.5">
              <label htmlFor="region-select" className="text-slate-400">
                Region:
              </label>
              <select
                id="region-select"
                value={region}
                onChange={(e) => setRegion(e.target.value)}
                disabled={isLoading}
                className="bg-[#090d16] border border-slate-700 rounded px-2 py-1 text-slate-200 text-xs focus:outline-none focus:border-indigo-500"
              >
                {REGIONS.map((r) => (
                  <option key={r.value} value={r.value}>
                    {r.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Max Reviews */}
            <div className="flex items-center gap-1.5">
              <label htmlFor="max-reviews-select" className="text-slate-400">
                Max Reviews:
              </label>
              <select
                id="max-reviews-select"
                value={maxReviews}
                onChange={(e) => setMaxReviews(Number(e.target.value))}
                disabled={isLoading}
                className="bg-[#090d16] border border-slate-700 rounded px-2 py-1 text-slate-200 text-xs focus:outline-none focus:border-indigo-500"
              >
                {REVIEW_LIMITS.map((limit) => (
                  <option key={limit} value={limit}>
                    {limit}
                  </option>
                ))}
              </select>
            </div>

            {/* Fresh Analysis */}
            <label className="flex items-center gap-1.5 cursor-pointer text-slate-300">
              <input
                type="checkbox"
                checked={fresh}
                onChange={(e) => setFresh(e.target.checked)}
                disabled={isLoading}
                className="rounded border-slate-700 bg-[#090d16] text-indigo-600 focus:ring-0 focus:ring-offset-0 w-3.5 h-3.5"
              />
              <span>Fresh retrieval</span>
            </label>
          </div>

          {/* Quick Examples */}
          <div className="flex items-center gap-1.5 text-[11px]">
            <span className="text-slate-400">Examples:</span>
            {POPULAR_QUERIES.map((preset) => (
              <button
                key={preset}
                type="button"
                onClick={() => handleSelectPreset(preset)}
                disabled={isLoading}
                className="px-1.5 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 transition text-[11px] disabled:opacity-50"
              >
                {preset}
              </button>
            ))}
          </div>
        </div>
      </form>
    </div>
  );
};
