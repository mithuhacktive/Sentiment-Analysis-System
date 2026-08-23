from __future__ import annotations
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class AnalyzeRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    fresh: bool = Field(False)
    region: Optional[str] = Field(None, max_length=8)
    max_reviews: Optional[int] = Field(None, ge=1, le=500)

    @field_validator("query")
    @classmethod
    def strip_and_validate_query(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("query must not be empty or whitespace only")
        return stripped


class FeedbackRequest(BaseModel):
    analysis_id: str = Field(..., description="UUID of the analysis")
    correct_label: str = Field(..., pattern="^(POSITIVE|NEGATIVE|NEUTRAL)$")
    comment: Optional[str] = Field(None, max_length=1000)


class ProductResolveRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    brand: Optional[str] = None
    model: Optional[str] = None
    region: Optional[str] = None
    url: Optional[str] = None