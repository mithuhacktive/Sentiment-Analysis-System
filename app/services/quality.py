from __future__ import annotations
import re
from dataclasses import dataclass


@dataclass
class QualityResult:
    label: str
    score: float
    spam_score: float
    flags: list[str]


_PROMO_PATTERNS = re.compile(
    r"(buy now|click here|limited offer|discount|promo code|best price|order now)",
    re.IGNORECASE,
)

_REPETITION_RE = re.compile(r"(\b\w+\b)(\s+\1){4,}", re.IGNORECASE)


class ReviewQualityScorer:
    MIN_WORDS = 5
    MAX_REPEAT_RATIO = 0.6

    def score(
        self,
        text: str,
        duplicate_status: str = "ORIGINAL",
        rating: float | None = None,
        sentiment_label: str | None = None,
    ) -> QualityResult:
        flags: list[str] = []
        penalties = 0.0

        words = text.split()
        word_count = len(words)

        # Too short
        if word_count < self.MIN_WORDS:
            flags.append("TOO_SHORT")
            penalties += 0.4

        # Promotional language — count matches, each hit adds penalty
        promo_matches = _PROMO_PATTERNS.findall(text)
        if promo_matches:
            flags.append("PROMOTIONAL")
            penalties += 0.20 * len(promo_matches)  # each promo phrase adds 0.20

        # Repetition
        if _REPETITION_RE.search(text):
            flags.append("REPETITIVE")
            penalties += 0.2

        # Unique word ratio
        if word_count > 10:
            unique_ratio = len(set(w.lower() for w in words)) / word_count
            if unique_ratio < 0.4:
                flags.append("LOW_UNIQUE_RATIO")
                penalties += 0.2

        # Duplicate status
        if duplicate_status == "EXACT_DUPLICATE":
            flags.append("EXACT_DUPLICATE")
            penalties += 0.5
        elif duplicate_status == "NEAR_DUPLICATE":
            flags.append("NEAR_DUPLICATE")
            penalties += 0.3

        # Rating/text mismatch
        if rating is not None and sentiment_label:
            if rating >= 4.5 and sentiment_label == "NEGATIVE":
                flags.append("RATING_TEXT_MISMATCH")
                penalties += 0.15
            elif rating <= 1.5 and sentiment_label == "POSITIVE":
                flags.append("RATING_TEXT_MISMATCH")
                penalties += 0.15

        spam_score = min(penalties, 1.0)
        quality_score = max(1.0 - spam_score, 0.0)

        if spam_score >= 0.7:
            label = "SUSPICIOUS"
        elif spam_score >= 0.35:
            label = "LOW_QUALITY"
        else:
            label = "NORMAL"

        return QualityResult(
            label=label,
            score=quality_score,
            spam_score=spam_score,
            flags=flags,
        )