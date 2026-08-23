from app.services.normalization import normalise_review
from app.ml.preprocessing import preprocess


def test_html_stripped():
    result = normalise_review("<p>Great product!</p>")
    assert "<p>" not in result["normalized_text"]
    assert "Great product" in result["normalized_text"]


def test_negation_preserved():
    result = preprocess("NOT good at all!!!")
    assert "NOT" in result or "not" in result.lower()


def test_whitespace_collapsed():
    result = normalise_review("too   many    spaces")
    assert "  " not in result["normalized_text"]


def test_content_hash_stable():
    r1 = normalise_review("Hello world")
    r2 = normalise_review("Hello world")
    assert r1["content_hash"] == r2["content_hash"]


def test_normalised_hash_ignores_case():
    r1 = normalise_review("Hello World")
    r2 = normalise_review("hello world")
    assert r1["normalised_hash"] == r2["normalised_hash"]


def test_boilerplate_removed():
    result = preprocess("Great product! Verified Purchase. Report Abuse")
    assert "Verified Purchase" not in result