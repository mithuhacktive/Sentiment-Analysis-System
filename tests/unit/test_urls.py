from app.utils.urls import is_valid_url, is_safe_url, normalise_url, extract_domain


def test_valid_https_url():
    assert is_valid_url("https://www.amazon.com/product/123") is True


def test_valid_http_url():
    assert is_valid_url("http://example.com") is True


def test_invalid_no_scheme():
    assert is_valid_url("amazon.com/product") is False


def test_invalid_empty():
    assert is_valid_url("") is False


def test_safe_url_passes():
    ok, reason = is_safe_url("https://www.amazon.com/dp/B09XS7JWHH")
    assert ok is True
    assert reason == "ok"


def test_localhost_blocked():
    ok, reason = is_safe_url("http://localhost:8080/admin")
    assert ok is False
    assert reason == "blocked_host"


def test_loopback_ip_blocked():
    ok, reason = is_safe_url("http://127.0.0.1/secret")
    assert ok is False


def test_private_ip_blocked():
    ok, reason = is_safe_url("http://192.168.1.1/router")
    assert ok is False
    assert reason == "private_ip"


def test_normalise_adds_https():
    result = normalise_url("example.com")
    assert result.startswith("https://")


def test_normalise_strips_whitespace():
    result = normalise_url("  https://example.com  ")
    assert result == "https://example.com"


def test_extract_domain():
    assert extract_domain("https://www.amazon.com/dp/123") == "amazon.com"


def test_extract_domain_no_www():
    assert extract_domain("https://reddit.com/r/headphones") == "reddit.com"