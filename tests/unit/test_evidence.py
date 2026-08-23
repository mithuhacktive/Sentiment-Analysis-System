from datetime import datetime, timezone, timedelta
from app.services.evidence import score_evidence, _freshness_score


def test_fresh_review_scores_high():
    score = _freshness_score(datetime.now(timezone.utc) - timedelta(days=10))
    assert score == 1.0


def test_old_review_scores_low():
    score = _freshness_score(datetime.now(timezone.utc) - timedelta(days=800))
    assert score == 0.35


def test_no_date_returns_midpoint():
    score = _freshness_score(None)
    assert score == 0.5


def test_score_evidence_known_source():
    result = score_evidence(
        review_id="r1",
        source="amazon",
        quality_score=0.9,
        language_confidence=0.95,
        duplicate_status="ORIGINAL",
        product_match_confidence=0.9,
        review_date=datetime.now(timezone.utc) - timedelta(days=5),
        sentiment_confidence=0.88,
    )
    assert result.score > 0.7
    assert "source_quality" in result.breakdown


def test_exact_duplicate_penalised():
    result = score_evidence(
        review_id="r2",
        source="amazon",
        quality_score=0.9,
        language_confidence=0.95,
        duplicate_status="EXACT_DUPLICATE",
        product_match_confidence=0.9,
        review_date=datetime.now(timezone.utc),
        sentiment_confidence=0.88,
    )
    assert result.score < 0.2


def test_unknown_source_gets_low_reliability():
    result = score_evidence(
        review_id="r3",
        source="randomsite",
        quality_score=0.5,
        language_confidence=0.7,
        duplicate_status="ORIGINAL",
        product_match_confidence=0.7,
        review_date=None,
        sentiment_confidence=0.6,
    )
    assert 0.0 < result.score < 0.7