from app.ml.preprocessing import preprocess, chunk_text, clean_html, normalise_whitespace


def test_clean_html_removes_tags():
    assert "<p>" not in clean_html("<p>Hello world</p>")
    assert "Hello world" in clean_html("<p>Hello world</p>")


def test_clean_html_decodes_entities():
    result = clean_html("Good &amp; Bad")
    assert "&amp;" not in result
    assert "Good & Bad" in result


def test_normalise_whitespace_collapses_spaces():
    result = normalise_whitespace("too   many    spaces")
    assert "  " not in result


def test_preprocess_full_pipeline():
    raw = "<p>  NOT good!!!  Verified Purchase  </p>"
    result = preprocess(raw)
    assert "<p>" not in result
    assert "NOT" in result
    assert "  " not in result


def test_chunk_text_short_text_single_chunk():
    chunks = chunk_text("Short text here", max_tokens=480)
    assert len(chunks) == 1
    assert chunks[0] == "Short text here"


def test_chunk_text_long_text_splits():
    long_text = " ".join(["word"] * 1000)
    chunks = chunk_text(long_text, max_tokens=100)
    assert len(chunks) > 1


def test_chunk_text_no_empty_chunks():
    long_text = " ".join(["word"] * 500)
    chunks = chunk_text(long_text, max_tokens=100)
    assert all(len(c.strip()) > 0 for c in chunks)


def test_chunk_text_empty_string():
    chunks = chunk_text("", max_tokens=480)
    assert len(chunks) >= 1