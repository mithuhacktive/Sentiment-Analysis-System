import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
} from 'recharts';
import { SourceInfo } from '../types/analysis';

interface SourceAnalysisProps {
  sources: SourceInfo[];
}

export const SourceAnalysis: React.FC<SourceAnalysisProps> = ({ sources }) => {
  if (!sources || sources.length === 0) {
    return (
      <div className="bg-[#0f1420] border border-slate-800 rounded-lg p-4 sm:p-5">
        <h3 className="text-base font-semibold text-white">Source Distribution</h3>
        <p className="text-slate-400 text-xs mt-1">No individual sources reported.</p>
      </div>
    );
  }

  const formatSourceName = (src: string) => {
    switch (src.toLowerCase()) {
      case 'fixture':
        return 'Local Knowledge / Fixture';
      case 'reddit':
        return 'Reddit';
      case 'serpapi':
        return 'Google Search / SerpApi';
      case 'url':
        return 'Direct Product Page';
      default:
        return src.charAt(0).toUpperCase() + src.slice(1);
    }
  };

  const chartData = sources.map((s) => ({
    source: formatSourceName(s.source),
    Positive: Math.round((s.sentiment_distribution.POSITIVE || 0) * 100),
    Neutral: Math.round((s.sentiment_distribution.NEUTRAL || 0) * 100),
    Negative: Math.round((s.sentiment_distribution.NEGATIVE || 0) * 100),
    reviews: s.review_count,
  }));

  return (
    <div className="bg-[#0f1420] border border-slate-800 rounded-lg p-4 sm:p-5 space-y-4">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div>
          <h3 className="text-base font-semibold text-white">Source Sentiment</h3>
          <p className="text-xs text-slate-400 mt-0.5">Sentiment split per review provider</p>
        </div>
        <span className="text-xs text-slate-400 font-mono">
          {sources.length} {sources.length === 1 ? 'source' : 'sources'}
        </span>
      </div>

      {/* Recharts Stacked Horizontal Bar */}
      <div className="h-44 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            layout="vertical"
            margin={{ top: 5, right: 20, left: 30, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
            <XAxis
              type="number"
              domain={[0, 100]}
              stroke="#64748b"
              tick={{ fill: '#94a3b8', fontSize: 10 }}
              unit="%"
            />
            <YAxis
              type="category"
              dataKey="source"
              stroke="#64748b"
              tick={{ fill: '#94a3b8', fontSize: 11 }}
              width={140}
            />
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const d = payload[0].payload;
                  return (
                    <div className="bg-[#0f172a] border border-slate-700 p-2.5 rounded shadow-lg text-xs space-y-1 min-w-[160px]">
                      <p className="font-semibold text-white">{d.source}</p>
                      <p className="text-slate-400">Total: {d.reviews} reviews</p>
                      <div className="text-[11px] pt-1 space-y-0.5">
                        <p className="text-emerald-400">Positive: {d.Positive}%</p>
                        <p className="text-amber-400">Neutral: {d.Neutral}%</p>
                        <p className="text-rose-400">Negative: {d.Negative}%</p>
                      </div>
                    </div>
                  );
                }
                return null;
              }}
            />
            <Legend
              wrapperStyle={{ fontSize: '11px', paddingTop: '6px' }}
              formatter={(val) => <span className="text-slate-300">{val}</span>}
            />
            <Bar dataKey="Positive" stackId="a" fill="#10b981" />
            <Bar dataKey="Neutral" stackId="a" fill="#f59e0b" />
            <Bar dataKey="Negative" stackId="a" fill="#f43f5e" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Compact Source List */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-2 border-t border-slate-800/80 text-xs">
        {sources.map((src, idx) => {
          const pos = Math.round((src.sentiment_distribution.POSITIVE || 0) * 100);
          const neu = Math.round((src.sentiment_distribution.NEUTRAL || 0) * 100);
          const neg = Math.round((src.sentiment_distribution.NEGATIVE || 0) * 100);
          return (
            <div key={idx} className="bg-[#090d16] border border-slate-800 rounded p-2.5 flex items-center justify-between">
              <div>
                <span className="font-medium text-slate-200 capitalize">{src.source}</span>
                <span className="text-[11px] text-slate-400 block">{src.review_count} reviews</span>
              </div>
              <div className="flex items-center gap-2 text-[11px] font-mono">
                <span className="text-emerald-400">{pos}%</span>
                <span className="text-slate-600">/</span>
                <span className="text-amber-400">{neu}%</span>
                <span className="text-slate-600">/</span>
                <span className="text-rose-400">{neg}%</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
