from __future__ import annotations
import hashlib
import re
import unicodedata
import xxhash


def content_hash(text: str) -> str:
    """SHA-256 of raw text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalised_hash(text: str) -> str:
    """Hash of aggressively normalised text for near-duplicate detection."""
    t = text.lower()
    t = unicodedata.normalize("NFKC", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"[^\w\s]", "", t)
    return xxhash.xxh64(t.encode("utf-8")).hexdigest()


def author_hash(author: str | None) -> str | None:
    if not author:
        return None
    return hashlib.sha256(author.strip().lower().encode()).hexdigest()[:16]