from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from app.config import get_settings

settings = get_settings()

# Source reliability scores — documented weights
SOURCE_RELIABILITY: dict[str, float] = {
    "amazon": 0.75,
    "reddit": 0.65,
    "bestbuy": 0.70,
    "walmart": 0.65,
    "gsmarena": 0.80,
    "rtings": 0.85,
    "fixture": 0.50,
    "generic": 0.55,
    "unknown": 0.40,
}


@dataclass
class EvidenceScore:
    review_id: str
    score: float
    breakdown: dict[str, float]


def _freshness_score(review_date: datetime | None) -> float:
    if review_date is None:
        return 0.5
    now = datetime.now(timezone.utc)
    if review_date.tzinfo is None:
        review_date = review_date.replace(tzinfo=timezone.utc)
    age_days = (now - review_date).days
    if age_days <= 30:
        return 1.0
    elif age_days <= 180:
        return 0.85
    elif age_days <= 365:
        return 0.70
    elif age_days <= 730:
        return 0.55
    else:
        return 0.35


def score_evidence(
    review_id: str,
    source: str,
    quality_score: float,
    language_confidence: float,
    duplicate_status: str,
    product_match_confidence: float,
    review_date: datetime | None,
    sentiment_confidence: float,
) -> EvidenceScore:
    """
    Weighted evidence scoring.
    All weights documented in config.
    """
    s = settings

    source_key = source.lower().split(".")[0] if source else "unknown"
    source_q = SOURCE_RELIABILITY.get(source_key, 0.50)

    freshness = _freshness_score(review_date)

    dup_penalty = 1.0
    if duplicate_status == "EXACT_DUPLICATE":
        dup_penalty = 0.1
    elif duplicate_status == "NEAR_DUPLICATE":
        dup_penalty = 0.3

    raw_score = (
        s.weight_source_quality * source_q
        + s.weight_review_quality * quality_score
        + s.weight_freshness * freshness
        + s.weight_sentiment_strength * sentiment_confidence
        + s.weight_product_match * product_match_confidence
        + s.weight_language_confidence * language_confidence
    ) * dup_penalty

    return EvidenceScore(
        review_id=review_id,
        score=round(min(max(raw_score, 0.0), 1.0), 4),
        breakdown={
            "source_quality": source_q,
            "review_quality": quality_score,
            "freshness": freshness,
            "sentiment_strength": sentiment_confidence,
            "product_match": product_match_confidence,
            "language_confidence": language_confidence,
            "duplicate_penalty": dup_penalty,
        },
    )