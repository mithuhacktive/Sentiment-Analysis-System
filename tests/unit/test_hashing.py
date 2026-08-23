from app.utils.hashing import content_hash, normalised_hash, author_hash


def test_content_hash_is_stable():
    assert content_hash("hello") == content_hash("hello")


def test_content_hash_differs_on_different_text():
    assert content_hash("hello") != content_hash("world")


def test_normalised_hash_ignores_case():
    assert normalised_hash("HELLO WORLD") == normalised_hash("hello world")


def test_normalised_hash_ignores_punctuation():
    assert normalised_hash("hello world!!!") == normalised_hash("hello world")


def test_normalised_hash_ignores_extra_spaces():
    assert normalised_hash("hello   world") == normalised_hash("hello world")


def test_author_hash_returns_none_for_none():
    assert author_hash(None) is None


def test_author_hash_stable():
    assert author_hash("UserA") == author_hash("UserA")


def test_author_hash_case_insensitive():
    assert author_hash("UserA") == author_hash("usera")


def test_author_hash_length():
    result = author_hash("testuser")
    assert len(result) == 16