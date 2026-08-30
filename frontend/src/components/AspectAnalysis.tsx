import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  CartesianGrid,
} from 'recharts';
import { AspectSentiment } from '../types/analysis';

interface AspectAnalysisProps {
  aspects: AspectSentiment[];
}

export const AspectAnalysis: React.FC<AspectAnalysisProps> = ({ aspects }) => {
  if (!aspects || aspects.length === 0) {
    return (
      <div className="bg-[#0f1420] border border-slate-800 rounded-lg p-4 sm:p-5">
        <h3 className="text-sm font-semibold text-white uppercase tracking-wider text-[11px] text-slate-400 mb-2">
          Aspect-Based Sentiment
        </h3>
        <p className="text-slate-400 text-xs italic">
          No distinct aspect sentiments identified in the retrieved reviews.
        </p>
      </div>
    );
  }

  const formatAspectName = (name: string) => {
    return name
      .replace(/_/g, ' ')
      .replace(/\b\w/g, (c) => c.toUpperCase());
  };

  const getSentimentColor = (label: string) => {
    switch (label) {
      case 'POSITIVE':
        return '#10b981'; // emerald-500
      case 'NEGATIVE':
        return '#f43f5e'; // rose-500
      default:
        return '#f59e0b'; // amber-500
    }
  };

  const getSentimentBadge = (label: string) => {
    switch (label) {
      case 'POSITIVE':
        return 'text-emerald-400 bg-emerald-950/40 border-emerald-800/60';
      case 'NEGATIVE':
        return 'text-rose-400 bg-rose-950/40 border-rose-800/60';
      default:
        return 'text-amber-400 bg-amber-950/40 border-amber-800/60';
    }
  };

  const chartData = aspects.map((a) => ({
    name: formatAspectName(a.name),
    confidence: Math.round(a.confidence * 1000) / 10,
    label: a.label,
    evidence_count: a.evidence_count,
  }));

  return (
    <div className="bg-[#0f1420] border border-slate-800 rounded-lg p-4 sm:p-5 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div>
          <h3 className="text-base font-semibold text-white">
            Aspect-Based Sentiment
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Key feature dimensions extracted from review text
          </p>
        </div>
        <div className="flex items-center gap-3 text-xs">
          <span className="flex items-center gap-1 text-slate-300">
            <span className="w-2 h-2 rounded-full bg-emerald-500"></span> Positive
          </span>
          <span className="flex items-center gap-1 text-slate-300">
            <span className="w-2 h-2 rounded-full bg-rose-500"></span> Negative
          </span>
          <span className="flex items-center gap-1 text-slate-300">
            <span className="w-2 h-2 rounded-full bg-amber-500"></span> Neutral
          </span>
        </div>
      </div>

      {/* Clean Aspect Table / List */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-slate-800 text-slate-400 uppercase text-[10px] tracking-wider">
              <th className="py-2 px-3 font-semibold">Aspect</th>
              <th className="py-2 px-3 font-semibold">Sentiment</th>
              <th className="py-2 px-3 font-semibold">Confidence</th>
              <th className="py-2 px-3 font-semibold text-right">Evidence</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {aspects.map((aspect, idx) => {
              const conf = Math.round(aspect.confidence * 1000) / 10;
              const color = getSentimentColor(aspect.label);
              return (
                <tr key={idx} className="hover:bg-slate-800/30 transition-colors">
                  <td className="py-2.5 px-3 font-medium text-slate-200">
                    {formatAspectName(aspect.name)}
                  </td>
                  <td className="py-2.5 px-3">
                    <span
                      className={`inline-block px-2 py-0.5 rounded border text-[11px] font-semibold ${getSentimentBadge(
                        aspect.label
                      )}`}
                    >
                      {aspect.label}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 w-48">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 bg-[#090d16] border border-slate-800 rounded-full h-1.5 overflow-hidden">
                        <div
                          className="h-full rounded-full"
                          style={{
                            width: `${conf}%`,
                            backgroundColor: color,
                          }}
                        />
                      </div>
                      <span className="text-slate-300 font-mono text-[11px] w-10 text-right">
                        {conf}%
                      </span>
                    </div>
                  </td>
                  <td className="py-2.5 px-3 text-right text-slate-400 font-mono text-[11px]">
                    {aspect.evidence_count} {aspect.evidence_count === 1 ? 'review' : 'reviews'}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Subtle Chart */}
      <div className="pt-2 border-t border-slate-800/80">
        <span className="text-xs text-slate-400 block mb-2 font-medium">
          Confidence Comparison
        </span>
        <div className="h-44 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={chartData}
              margin={{ top: 5, right: 10, left: -20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
              <XAxis
                dataKey="name"
                stroke="#64748b"
                tick={{ fill: '#94a3b8', fontSize: 11 }}
                interval={0}
              />
              <YAxis
                stroke="#64748b"
                tick={{ fill: '#94a3b8', fontSize: 10 }}
                domain={[0, 100]}
              />
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const d = payload[0].payload;
                    return (
                      <div className="bg-[#0f172a] border border-slate-700 p-2.5 rounded shadow-lg text-xs space-y-1">
                        <p className="font-semibold text-white">{d.name}</p>
                        <p className="text-slate-300">
                          Sentiment: <span className="font-semibold" style={{ color: getSentimentColor(d.label) }}>{d.label}</span>
                        </p>
                        <p className="text-slate-400">Confidence: {d.confidence}%</p>
                        <p className="text-slate-400">Evidence: {d.evidence_count} reviews</p>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Bar dataKey="confidence" radius={[3, 3, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={getSentimentColor(entry.label)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
