from __future__ import annotations
import re
import unicodedata
from html import unescape


# Patterns that indicate boilerplate
_BOILERPLATE_RE = re.compile(
    r"(verified purchase|helpful\?\s*\d+|report abuse|read more|see all reviews)",
    re.IGNORECASE,
)


def clean_html(text: str) -> str:
    """Remove HTML tags and decode entities."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    return text


def normalise_whitespace(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fix_encoding(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    return text


def remove_boilerplate(text: str) -> str:
    return _BOILERPLATE_RE.sub("", text).strip()


def preprocess(text: str) -> str:
    """
    Full preprocessing pipeline.
    Preserves negation, punctuation, emojis.
    Does NOT lowercase — model handles casing.
    """
    text = fix_encoding(text)
    text = clean_html(text)
    text = remove_boilerplate(text)
    text = normalise_whitespace(text)
    return text


def chunk_text(text: str, max_tokens: int = 480, overlap: int = 50) -> list[str]:
    """
    Split long text into overlapping word-level chunks.
    Rough word count proxy (1 word ≈ 1.3 tokens).
    """
    words = text.split()
    word_limit = int(max_tokens / 1.3)
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + word_limit, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start += word_limit - overlap
    return chunks if chunks else [text]