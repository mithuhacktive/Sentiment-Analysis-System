from app.services.calibration import calibrate_confidence, confidence_label


def test_large_sample_no_penalty():
    result = calibrate_confidence(0.90, "POSITIVE", n_reviews=50)
    assert result >= 0.85


def test_small_sample_penalised():
    result = calibrate_confidence(0.90, "POSITIVE", n_reviews=3)
    assert result < 0.80


def test_very_small_sample_heavily_penalised():
    result = calibrate_confidence(0.90, "POSITIVE", n_reviews=1)
    assert result < 0.70


def test_confidence_never_exceeds_ceiling():
    result = calibrate_confidence(1.0, "POSITIVE", n_reviews=1000)
    assert result <= 0.98


def test_confidence_never_below_floor():
    result = calibrate_confidence(0.0, "NEGATIVE", n_reviews=100)
    assert result >= 0.05


def test_high_label():
    assert confidence_label(0.85) == "HIGH"


def test_moderate_label():
    assert confidence_label(0.65) == "MODERATE"


def test_low_label():
    assert confidence_label(0.40) == "LOW"