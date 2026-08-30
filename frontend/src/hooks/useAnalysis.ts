import { useState, useRef } from 'react';
import { api, parseApiError } from '../services/api';
import {
  AnalyzeRequest,
  AnalysisResponse,
  FeedbackRequest,
  FeedbackResponse,
  ApiError,
  SentimentLabel,
} from '../types/analysis';

export function useAnalysis() {
  const [data, setData] = useState<AnalysisResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [loadingStage, setLoadingStage] = useState<string>('');
  const [error, setError] = useState<ApiError | null>(null);
  const [feedbackSuccess, setFeedbackSuccess] = useState<string | null>(null);
  const [isSubmittingFeedback, setIsSubmittingFeedback] = useState<boolean>(false);
  const [feedbackError, setFeedbackError] = useState<string | null>(null);

  const stageTimerRef = useRef<NodeJS.Timeout[]>([]);

  const clearTimers = () => {
    stageTimerRef.current.forEach((t) => clearTimeout(t));
    stageTimerRef.current = [];
  };

  const startLoadingStages = () => {
    clearTimers();
    setLoadingStage('Analyzing product query and identity...');

    const t1 = setTimeout(() => {
      setLoadingStage('Retrieving reviews from sources & adapters...');
    }, 700);

    const t2 = setTimeout(() => {
      setLoadingStage('Deduplicating & scoring evidence quality...');
    }, 1600);

    const t3 = setTimeout(() => {
      setLoadingStage('Running RoBERTa sentiment & aspect extraction...');
    }, 2500);

    const t4 = setTimeout(() => {
      setLoadingStage('Aggregating calibrated product intelligence...');
    }, 3600);

    stageTimerRef.current = [t1, t2, t3, t4];
  };

  const runAnalysis = async (request: AnalyzeRequest) => {
    setIsLoading(true);
    setError(null);
    setFeedbackSuccess(null);
    setFeedbackError(null);
    startLoadingStages();

    try {
      const response = await api.analyze(request);
      setData(response);
      return response;
    } catch (err: unknown) {
      const parsed = parseApiError(err);
      setError(parsed);
      setData(null);
      throw parsed;
    } finally {
      clearTimers();
      setIsLoading(false);
      setLoadingStage('');
    }
  };

  const submitFeedback = async (
    correctLabel: SentimentLabel,
    comment?: string
  ): Promise<FeedbackResponse | null> => {
    if (!data?.analysis_id) return null;

    setIsSubmittingFeedback(true);
    setFeedbackError(null);
    setFeedbackSuccess(null);

    const req: FeedbackRequest = {
      analysis_id: data.analysis_id,
      correct_label: correctLabel,
      comment: comment?.trim() || null,
    };

    try {
      const res = await api.submitFeedback(req);
      setFeedbackSuccess(res.message || 'Feedback recorded successfully. Thank you!');
      return res;
    } catch (err: unknown) {
      const parsed = parseApiError(err);
      setFeedbackError(parsed.message);
      return null;
    } finally {
      setIsSubmittingFeedback(false);
    }
  };

  const resetAnalysis = () => {
    clearTimers();
    setData(null);
    setError(null);
    setIsLoading(false);
    setFeedbackSuccess(null);
    setFeedbackError(null);
  };

  return {
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
  };
}
