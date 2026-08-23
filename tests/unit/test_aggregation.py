from app.services.aggregation import aggregate, compute_conflict


def _review(label, score=0.85, source="amazon", dup="ORIGINAL"):
    probs = {"POSITIVE": 0.0, "NEGATIVE": 0.0, "NEUTRAL": 0.0}
    probs[label] = score
    remaining = (1.0 - score) / 2
    for k in probs:
        if probs[k] == 0.0:
            probs[k] = remaining
    return {
        "id": "x",
        "label": label,
        "probabilities": probs,
        "evidence_score": 0.8,
        "source": source,
        "duplicate_status": dup,
    }


def test_positive_majority():
    reviews = [_review("POSITIVE")] * 8 + [_review("NEGATIVE")] * 2
    result = aggregate(reviews, product_match_confidence=0.9, n_independent=10)
    assert result.label == "POSITIVE"
    assert result.abstain is False


def test_negative_majority():
    # Use very high score and large count so calibration keeps confidence above threshold
    reviews = [_review("NEGATIVE", score=0.95)] * 9 + [_review("POSITIVE", score=0.95)] * 1
    result = aggregate(reviews, product_match_confidence=0.9, n_independent=10)
    assert result.label == "NEGATIVE"
    assert result.abstain is False


def test_abstain_no_reviews():
    result = aggregate([], product_match_confidence=0.9, n_independent=0)
    assert result.abstain is True
    assert result.abstain_reason == "NO_REVIEWS"


def test_abstain_few_reviews():
    reviews = [_review("POSITIVE")]
    result = aggregate(reviews, product_match_confidence=0.9, n_independent=1)
    assert result.abstain is True


def test_conflict_detection():
    dist = {
        "source_a": {"POSITIVE": 1.0, "NEGATIVE": 0.0, "NEUTRAL": 0.0},
        "source_b": {"POSITIVE": 0.0, "NEGATIVE": 1.0, "NEUTRAL": 0.0},
    }
    level, score = compute_conflict(dist)
    assert level in ("MODERATE", "HIGH")


def test_low_product_confidence_abstains():
    reviews = [_review("POSITIVE")] * 10
    result = aggregate(reviews, product_match_confidence=0.3, n_independent=10)
    assert result.abstain is True
    assert result.abstain_reason == "PRODUCT_MATCH_UNCERTAIN"


def test_conflict_penalises_confidence():
    pos_reviews = [_review("POSITIVE", source="amazon")] * 5
    neg_reviews = [_review("NEGATIVE", source="reddit")] * 5
    result = aggregate(pos_reviews + neg_reviews, product_match_confidence=0.9, n_independent=10)
    assert result.conflict_level in ("MODERATE", "HIGH")


def test_weighted_aggregation_uses_evidence_score():
    # High evidence score review should dominate low evidence score review
    strong = _review("POSITIVE", score=0.95)
    strong["evidence_score"] = 0.95
    weak = _review("NEGATIVE", score=0.95)
    weak["evidence_score"] = 0.05
    reviews = [strong] * 5 + [weak] * 5
    result = aggregate(reviews, product_match_confidence=0.9, n_independent=10)
    # Strong positive evidence should win despite equal count
    assert result.label == "POSITIVE"