from __future__ import annotations
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, Field, ConfigDict


class ProductInfo(BaseModel):
    name: str
    brand: Optional[str] = None
    model: Optional[str] = None
    variant: Optional[str] = None
    region: Optional[str] = None
    confidence: float
    resolution_status: str


class OverallSentiment(BaseModel):
    label: str
    confidence: float
    calibrated: bool


class AspectSentiment(BaseModel):
    name: str
    label: str
    confidence: float
    evidence_count: int


class EvidenceSummary(BaseModel):
    reviews_analyzed: int
    independent_reviews: int
    sources: int
    duplicates: int
    suspicious_reviews: int
    conflict_level: str


class SourceInfo(BaseModel):
    source: str
    url: Optional[str] = None
    review_count: int
    sentiment_distribution: dict[str, float]


class PipelineInfo(BaseModel):
    version: str
    model: str
    retrieved_at: datetime
    processing_time_ms: float
    cache_used: bool
    data_freshness: str


class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    product: Optional[ProductInfo] = None
    overall: Optional[OverallSentiment] = None
    aspects: list[AspectSentiment] = Field(default_factory=list)
    evidence: Optional[EvidenceSummary] = None
    sources: list[SourceInfo] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    pipeline: Optional[PipelineInfo] = None


class HealthResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    status: str
    version: str
    model_loaded: bool
    database_ok: bool
    offline_mode: bool


class ProductResolveResponse(BaseModel):
    product_id: str
    canonical_name: str
    brand: Optional[str] = None
    model: Optional[str] = None
    variant: Optional[str] = None
    region: Optional[str] = None
    confidence: float
    status: str


class FeedbackResponse(BaseModel):
    accepted: bool
    message: str