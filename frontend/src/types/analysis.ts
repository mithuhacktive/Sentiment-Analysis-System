export type SentimentLabel = 'POSITIVE' | 'NEGATIVE' | 'NEUTRAL';

export type ResolutionStatus = 'EXACT' | 'FUZZY' | 'AMBIGUOUS' | 'NOT_FOUND' | 'RESOLVED' | string;

export type ConflictLevel = 'LOW' | 'MEDIUM' | 'HIGH' | string;

export type AnalysisStatus = 'COMPLETED' | 'INSUFFICIENT_EVIDENCE' | 'FAILED' | string;

export interface AnalyzeRequest {
  query: string;
  fresh?: boolean;
  region?: string | null;
  max_reviews?: number | null;
}

export interface ProductInfo {
  name: string;
  brand: string | null;
  model: string | null;
  variant: string | null;
  region: string | null;
  confidence: number;
  resolution_status: ResolutionStatus;
}

export interface OverallSentiment {
  label: SentimentLabel;
  confidence: number;
  calibrated: boolean;
}

export interface AspectSentiment {
  name: string;
  label: SentimentLabel;
  confidence: number;
  evidence_count: number;
}

export interface EvidenceSummary {
  reviews_analyzed: number;
  independent_reviews: number;
  sources: number;
  duplicates: number;
  suspicious_reviews: number;
  conflict_level: ConflictLevel;
}

export interface SourceInfo {
  source: string;
  url?: string | null;
  review_count: number;
  sentiment_distribution: {
    POSITIVE: number;
    NEGATIVE: number;
    NEUTRAL: number;
    [key: string]: number;
  };
}

export interface PipelineInfo {
  version: string;
  model: string;
  retrieved_at: string;
  processing_time_ms: number;
  cache_used: boolean;
  data_freshness: string;
}

export interface AnalysisResponse {
  analysis_id: string;
  status: AnalysisStatus;
  product: ProductInfo | null;
  overall: OverallSentiment | null;
  aspects: AspectSentiment[];
  evidence: EvidenceSummary | null;
  sources: SourceInfo[];
  limitations: string[];
  pipeline: PipelineInfo | null;
}

export interface HealthResponse {
  status: string;
  version: string;
  model_loaded: boolean;
  database_ok: boolean;
  offline_mode: boolean;
}

export interface ReadyResponse {
  ready: boolean;
  reason?: string;
}

export interface FeedbackRequest {
  analysis_id: string;
  correct_label: SentimentLabel;
  comment?: string | null;
}

export interface FeedbackResponse {
  accepted: boolean;
  message: string;
}

export interface ApiError {
  message: string;
  status?: number;
  detail?: string | Record<string, unknown> | Array<{ msg?: string; loc?: string[] }>;
}
