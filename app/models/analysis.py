from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, DateTime, Float, Text, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Analysis(Base):
    __tablename__ = "analyses"

    analysis_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    product_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    query: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="PENDING")
    overall_label: Mapped[str | None] = mapped_column(String(16), nullable=True)
    overall_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    calibrated: Mapped[bool] = mapped_column(default=False)
    reviews_analyzed: Mapped[int] = mapped_column(Integer, default=0)
    independent_reviews: Mapped[int] = mapped_column(Integer, default=0)
    duplicates_found: Mapped[int] = mapped_column(Integer, default=0)
    suspicious_reviews: Mapped[int] = mapped_column(Integer, default=0)
    sources_attempted: Mapped[int] = mapped_column(Integer, default=0)
    sources_successful: Mapped[int] = mapped_column(Integer, default=0)
    conflict_level: Mapped[str | None] = mapped_column(String(32), nullable=True)
    cache_used: Mapped[bool] = mapped_column(default=False)
    pipeline_version: Mapped[str] = mapped_column(String(32), default="1.0.0")
    model_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    processing_time_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    result_json: Mapped[str | None] = mapped_column(Text, nullable=True)  # full JSON blob
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())