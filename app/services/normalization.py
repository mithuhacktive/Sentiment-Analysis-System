from __future__ import annotations
from app.ml.preprocessing import preprocess, chunk_text
from app.utils.hashing import content_hash, normalised_hash


def normalise_review(text: str) -> dict:
    """
    Returns normalised text plus metadata.
    Never mutates the original.
    """
    cleaned = preprocess(text)
    return {
        "normalized_text": cleaned,
        "content_hash": content_hash(text),
        "normalised_hash": normalised_hash(cleaned),
        "original_length": len(text),
        "normalised_length": len(cleaned),
    }


def prepare_chunks(text: str, max_tokens: int = 480) -> list[str]:
    return chunk_text(text, max_tokens=max_tokens)