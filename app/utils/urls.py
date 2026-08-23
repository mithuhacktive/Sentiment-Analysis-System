from __future__ import annotations
import ipaddress
import re
from urllib.parse import urlparse


ALLOWED_SCHEMES = {"http", "https"}
BLOCKED_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}


def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in ALLOWED_SCHEMES and bool(parsed.netloc)
    except Exception:
        return False


def is_safe_url(url: str) -> tuple[bool, str]:
    """SSRF protection."""
    try:
        parsed = urlparse(url)
        host = parsed.hostname or ""
        if not host:
            return False, "no_host"
        if host in BLOCKED_HOSTS:
            return False, "blocked_host"
        try:
            addr = ipaddress.ip_address(host)
            if addr.is_private or addr.is_loopback or addr.is_link_local:
                return False, "private_ip"
        except ValueError:
            pass  # Not an IP, continue
        return True, "ok"
    except Exception as e:
        return False, str(e)


def normalise_url(url: str) -> str:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def extract_domain(url: str) -> str:
    try:
        return urlparse(url).netloc.lower().lstrip("www.")
    except Exception:
        return ""