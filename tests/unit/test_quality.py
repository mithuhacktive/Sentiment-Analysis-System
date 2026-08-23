from app.services.quality import ReviewQualityScorer


def test_normal_review():
    scorer = ReviewQualityScorer()
    result = scorer.score("The battery life on this headphone is excellent. Very comfortable to wear.")
    assert result.label == "NORMAL"
    assert result.spam_score < 0.35


def test_spam_detected():
    scorer = ReviewQualityScorer()
    result = scorer.score("Buy now! Click here! Limited offer! Best price! Promo code!")
    assert result.label in ("SUSPICIOUS", "LOW_QUALITY")
    assert "PROMOTIONAL" in result.flags


def test_too_short():
    scorer = ReviewQualityScorer()
    result = scorer.score("ok")
    assert "TOO_SHORT" in result.flags


def test_duplicate_penalised():
    scorer = ReviewQualityScorer()
    result = scorer.score("Good product overall.", duplicate_status="EXACT_DUPLICATE")
    assert result.spam_score > 0.3


def test_rating_mismatch():
    scorer = ReviewQualityScorer()
    result = scorer.score(
        "Absolutely terrible experience. Would not recommend to anyone.",
        rating=5.0,
        sentiment_label="NEGATIVE",
    )
    assert "RATING_TEXT_MISMATCH" in result.flags