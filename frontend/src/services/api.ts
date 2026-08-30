import axios, { AxiosError } from 'axios';
import {
  AnalyzeRequest,
  AnalysisResponse,
  FeedbackRequest,
  FeedbackResponse,
  HealthResponse,
  ReadyResponse,
  ApiError,
} from '../types/analysis';

const apiClient = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 35000,
});

export function parseApiError(error: unknown): ApiError {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<{ detail?: unknown; error?: string }>;
    const status = axiosError.response?.status;
    const data = axiosError.response?.data;

    if (status === 422 && Array.isArray(data?.detail)) {
      const msg = data.detail.map((d: { msg?: string; loc?: string[] }) => d.msg || 'Invalid field').join(', ');
      return {
        message: `Validation Error: ${msg}`,
        status,
        detail: data.detail,
      };
    }

    if (data?.detail && typeof data.detail === 'string') {
      return {
        message: data.detail,
        status,
        detail: data.detail,
      };
    }

    if (data?.error && typeof data.error === 'string') {
      return {
        message: data.error,
        status,
        detail: data,
      };
    }

    if (axiosError.code === 'ECONNABORTED') {
      return {
        message: 'Request timed out while analyzing. The model or data sources may still be processing.',
        status,
      };
    }

    if (!axiosError.response) {
      return {
        message: 'Unable to connect to SentiGuard backend server (http://127.0.0.1:8000). Please check if backend is running.',
        status: 0,
      };
    }

    return {
      message: axiosError.message || 'An unexpected API error occurred.',
      status,
    };
  }

  if (error instanceof Error) {
    return { message: error.message };
  }

  return { message: 'An unknown error occurred.' };
}

export const api = {
  async getHealth(): Promise<HealthResponse> {
    const { data } = await apiClient.get<HealthResponse>('/health');
    return data;
  },

  async getReady(): Promise<ReadyResponse> {
    const { data } = await apiClient.get<ReadyResponse>('/health/ready');
    return data;
  },

  async analyze(request: AnalyzeRequest): Promise<AnalysisResponse> {
    const { data } = await apiClient.post<AnalysisResponse>('/analyze', request);
    return data;
  },

  async submitFeedback(request: FeedbackRequest): Promise<FeedbackResponse> {
    const { data } = await apiClient.post<FeedbackResponse>('/feedback', request);
    return data;
  },
};
