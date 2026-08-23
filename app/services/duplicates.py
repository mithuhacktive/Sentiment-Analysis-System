from __future__ import annotations
import logging
from dataclasses import dataclass, field
from app.utils.hashing import content_hash, normalised_hash

logger = logging.getLogger(__name__)


@dataclass
class ReviewForDedup:
    review_id: str
    content_hash: str
    normalised_hash: str
    text: str = ""


@dataclass
class DedupResult:
    review_id: str
    status: str  # ORIGINAL | EXACT_DUPLICATE | NEAR_DUPLICATE
    duplicate_of: str | None = None


class DuplicateDetector:
    """
    Two-level duplicate detection:
    1. Exact hash match
    2. Normalised hash match (handles whitespace/case variations)

    Avoids O(n²) semantic comparison on large sets.
    """

    def detect(self, reviews: list[ReviewForDedup]) -> list[DedupResult]:
        seen_content: dict[str, str] = {}      # hash → first review_id
        seen_normalised: dict[str, str] = {}
        results: list[DedupResult] = []

        for rev in reviews:
            if rev.content_hash in seen_content:
                results.append(DedupResult(
                    review_id=rev.review_id,
                    status="EXACT_DUPLICATE",
                    duplicate_of=seen_content[rev.content_hash],
                ))
                continue

            if rev.normalised_hash in seen_normalised:
                results.append(DedupResult(
                    review_id=rev.review_id,
                    status="NEAR_DUPLICATE",
                    duplicate_of=seen_normalised[rev.normalised_hash],
                ))
                continue

            seen_content[rev.content_hash] = rev.review_id
            seen_normalised[rev.normalised_hash] = rev.review_id
            results.append(DedupResult(
                review_id=rev.review_id,
                status="ORIGINAL",
            ))

        return results