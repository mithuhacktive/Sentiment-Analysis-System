from __future__ import annotations
from datetime import datetime
from sqlalchemy import String, DateTime, Float, Text, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Review(Base):
    __tablename__ = "reviews"

    review_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    product_id: Mapped[str] = mapped_column(String(64), index=True)
    source: Mapped[str] = mapped_column(String(64))
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    external_id: Mapped[str | None] = mapped_column(String(256), nullable=True)
    review_text: Mapped[str] = mapped_column(Text)
    normalized_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    language: Mapped[str | None] = mapped_column(String(16), nullable=True)
    language_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    review_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    author_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    content_hash: Mapped[str] = mapped_column(String(64), index=True)
    normalised_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    # Quality
    quality_label: Mapped[str | None] = mapped_column(String(32), nullable=True)
    quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    spam_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    duplicate_status: Mapped[str | None] = mapped_column(String(32), nullable=True)
    # Sentiment
    sentiment_label: Mapped[str | None] = mapped_column(String(16), nullable=True)
    sentiment_confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    sentiment_positive: Mapped[float | None] = mapped_column(Float, nullable=True)
    sentiment_negative: Mapped[float | None] = mapped_column(Float, nullable=True)
    sentiment_neutral: Mapped[float | None] = mapped_column(Float, nullable=True)
    # Evidence
    evidence_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    chunk_count: Mapped[int] = mapped_column(Integer, default=1)