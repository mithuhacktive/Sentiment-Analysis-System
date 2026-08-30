import React from 'react';
import { Search } from 'lucide-react';

interface EmptyStateProps {
  onSelectQuery: (query: string) => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({ onSelectQuery }) => {
  const sampleSearches = [
    { title: 'Sony WH-1000XM5', category: 'Audio' },
    { title: 'Apple iPhone 15 Pro', category: 'Smartphone' },
    { title: 'MacBook Air M3', category: 'Laptop' },
    { title: 'Bose QuietComfort Ultra', category: 'Headphones' },
  ];

  const features = [
    {
      title: 'Sentiment Inference',
      desc: 'RoBERTa model evaluation with Bayesian calibration.',
    },
    {
      title: 'Aspect Extraction',
      desc: 'Granular scoring across battery, performance, comfort, sound, and build.',
    },
    {
      title: 'Evidence Verification',
      desc: 'Deduplication, bot filtering, and source conflict detection.',
    },
    {
      title: 'Multi-Source Aggregation',
      desc: 'Combines Reddit, direct URL scraping, and search indexes.',
    },
  ];

  return (
    <div className="space-y-4 py-2">
      {/* Onboarding Panel */}
      <div className="bg-[#0f1420] border border-slate-800 rounded-lg p-6 sm:p-8 text-center space-y-4">
        <div className="max-w-xl mx-auto space-y-2">
          <h2 className="text-lg sm:text-xl font-bold text-white tracking-tight">
            Product Sentiment Intelligence
          </h2>
          <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
            Enter a product name, keyword, or product URL to analyze customer sentiment, aspect breakdowns, evidence quality, and multi-source consensus.
          </p>
        </div>

        {/* Quick Launch Buttons */}
        <div className="pt-2">
          <span className="text-xs text-slate-400 block mb-2">
            Try a sample query:
          </span>
          <div className="flex flex-wrap justify-center gap-2">
            {sampleSearches.map((item) => (
              <button
                key={item.title}
                onClick={() => onSelectQuery(item.title)}
                className="px-3 py-1.5 bg-[#090d16] hover:bg-slate-800 border border-slate-800 hover:border-slate-700 rounded text-xs text-slate-300 hover:text-white transition flex items-center gap-1.5"
              >
                <Search className="w-3 h-3 text-slate-400" />
                <span>{item.title}</span>
                <span className="text-[10px] text-slate-400">({item.category})</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Feature Capabilities Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {features.map((feat, idx) => (
          <div
            key={idx}
            className="bg-[#0f1420] border border-slate-800 rounded-lg p-3.5 space-y-1 text-xs"
          >
            <h4 className="font-semibold text-slate-200">{feat.title}</h4>
            <p className="text-slate-400 text-[11px] leading-relaxed">{feat.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
