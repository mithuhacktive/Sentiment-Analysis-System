from app.services.duplicates import DuplicateDetector, ReviewForDedup
from app.utils.hashing import content_hash, normalised_hash


def _make(rid, text):
    return ReviewForDedup(
        review_id=rid,
        content_hash=content_hash(text),
        normalised_hash=normalised_hash(text),
        text=text,
    )


def test_exact_duplicate_detected():
    det = DuplicateDetector()
    reviews = [_make("r1", "Great product"), _make("r2", "Great product")]
    results = det.detect(reviews)
    assert results[0].status == "ORIGINAL"
    assert results[1].status == "EXACT_DUPLICATE"
    assert results[1].duplicate_of == "r1"


def test_near_duplicate_detected():
    det = DuplicateDetector()
    reviews = [_make("r1", "Great product!!!"), _make("r2", "GREAT PRODUCT")]
    results = det.detect(reviews)
    assert results[0].status == "ORIGINAL"
    assert results[1].status in ("NEAR_DUPLICATE", "EXACT_DUPLICATE")


def test_unique_reviews_pass():
    det = DuplicateDetector()
    reviews = [
        _make("r1", "Battery life is excellent"),
        _make("r2", "Build quality feels cheap"),
        _make("r3", "Sound is amazing for the price"),
    ]
    results = det.detect(reviews)
    assert all(r.status == "ORIGINAL" for r in results)