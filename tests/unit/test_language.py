from app.services.language import detect_language


def test_english_detected():
    result = detect_language("This product has excellent battery life and great sound quality.")
    assert result.language == "en"
    assert result.confidence > 0.5


def test_very_short_text_uncertain():
    result = detect_language("ok")
    assert result.status == "LANGUAGE_UNCERTAIN"


def test_empty_like_text():
    result = detect_language("   ")
    assert result.status == "LANGUAGE_UNCERTAIN"


def test_result_has_all_fields():
    result = detect_language("The noise cancellation on these headphones is superb.")
    assert hasattr(result, "language")
    assert hasattr(result, "confidence")
    assert hasattr(result, "status")