import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { SearchPanel } from './components/SearchPanel';
import { ExecutiveSummary } from './components/ExecutiveSummary';
import { AspectAnalysis } from './components/AspectAnalysis';
import { EvidenceQuality } from './components/EvidenceQuality';
import { SourceAnalysis } from './components/SourceAnalysis';
import { PipelineInfo } from './components/PipelineInfo';
import { Limitations } from './components/Limitations';
import { FeedbackSection } from './components/FeedbackModal';
import { LoadingState } from './components/LoadingState';
import { EmptyState } from './components/EmptyState';
import { ErrorState } from './components/ErrorState';
import { useBackendHealth } from './hooks/useBackendHealth';
import { useAnalysis } from './hooks/useAnalysis';
import { AnalyzeRequest, SentimentLabel } from './types/analysis';
import { AlertCircle } from 'lucide-react';

export const App: React.FC = () => {
  const { health, isConnected, isChecking, refreshHealth } = useBackendHealth(12000);
  const {
    data,
    isLoading,
    loadingStage,
    error,
    feedbackSuccess,
    feedbackError,
    isSubmittingFeedback,
    runAnalysis,
    submitFeedback,
    resetAnalysis,
  } = useAnalysis();

  const [lastRequest, setLastRequest] = useState<AnalyzeRequest | null>(null);

  const handleAnalyze = async (request: AnalyzeRequest) => {
    setLastRequest(request);
    try {
      await runAnalysis(request);
    } catch {
      // Handled via useAnalysis error state
    }
  };

  const handleRetry = () => {
    if (lastRequest) {
      handleAnalyze(lastRequest);
    }
  };

  const handleSelectPreset = (query: string) => {
    const req: AnalyzeRequest = { query, fresh: false, max_reviews: 25 };
    handleAnalyze(req);
  };

  const handleFeedbackSubmit = (label: SentimentLabel, comment?: string) => {
    submitFeedback(label, comment);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#0b0f17] text-slate-200">
      {/* Header */}
      <Navbar
        health={health}
        isConnected={isConnected}
        isChecking={isChecking}
        onRefreshHealth={refreshHealth}
      />

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-5 space-y-4">
        {/* Search / Analysis Controls */}
        <SearchPanel
          isLoading={isLoading}
          onAnalyze={handleAnalyze}
          initialQuery={lastRequest?.query || ''}
        />

        {/* Backend Offline Warning */}
        {isConnected === false && !isLoading && (
          <div className="bg-rose-950/40 border border-rose-800/60 rounded-lg p-3 flex items-center gap-2.5 text-xs text-rose-300">
            <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
            <span>
              Backend is currently offline at <code className="bg-[#090d16] px-1 py-0.5 rounded font-mono">http://127.0.0.1:8000</code>. Please check your FastAPI service.
            </span>
          </div>
        )}

        {/* Dynamic Display State */}
        {isLoading ? (
          <LoadingState currentStage={loadingStage} />
        ) : error ? (
          <ErrorState
            error={error}
            onRetry={lastRequest ? handleRetry : undefined}
            onReset={resetAnalysis}
          />
        ) : data ? (
          <div className="space-y-4">
            {/* 1. Result Summary (Two Columns) */}
            <ExecutiveSummary
              product={data.product}
              overall={data.overall}
              status={data.status}
            />

            {/* 2. Aspect-Based Sentiment */}
            <AspectAnalysis aspects={data.aspects} />

            {/* 3. Evidence / Quality Breakdown */}
            <EvidenceQuality evidence={data.evidence} />

            {/* 4. Source Distribution */}
            <SourceAnalysis sources={data.sources} />

            {/* 5. Pipeline Telemetry */}
            <PipelineInfo
              pipeline={data.pipeline}
              analysisId={data.analysis_id}
            />

            {/* 6. Limitations */}
            <Limitations limitations={data.limitations} />

            {/* 7. Feedback */}
            <FeedbackSection
              analysisId={data.analysis_id}
              isSubmitting={isSubmittingFeedback}
              successMessage={feedbackSuccess}
              errorMessage={feedbackError}
              onSubmit={handleFeedbackSubmit}
            />
          </div>
        ) : (
          <EmptyState onSelectQuery={handleSelectPreset} />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-[#0f1420] py-4 mt-8 text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>SentiGuard — Product Sentiment Intelligence</span>
          <span className="text-[11px] text-slate-400">
            RoBERTa Transformer + Bayesian Calibration
          </span>
        </div>
      </footer>
    </div>
  );
};
