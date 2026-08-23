from __future__ import annotations
import logging
from dataclasses import dataclass
from app.ml.model import get_model, SentimentResult
from app.ml.preprocessing import chunk_text

logger = logging.getLogger(__name__)


@dataclass
class ReviewSentiment:
    label: str
    confidence: float
    probabilities: dict[str, float]
    chunk_count: int


def _aggregate_chunks(chunk_results: list[SentimentResult]) -> ReviewSentiment:
    """Average probabilities across chunks."""
    avg: dict[str, float] = {"POSITIVE": 0.0, "NEGATIVE": 0.0, "NEUTRAL": 0.0}
    for r in chunk_results:
        for k, v in r.probabilities.items():
            avg[k] = avg.get(k, 0.0) + v
    n = len(chunk_results)
    for k in avg:
        avg[k] /= n
    label = max(avg, key=lambda x: avg[x])
    return ReviewSentiment(
        label=label,
        confidence=avg[label],
        probabilities=avg,
        chunk_count=n,
    )


class SentimentService:
    def __init__(self) -> None:
        self._model = get_model()

    def ensure_loaded(self) -> None:
        if not self._model.is_loaded:
            self._model.load()

    def analyse_text(self, text: str) -> ReviewSentiment:
        self.ensure_loaded()
        chunks = chunk_text(text, max_tokens=480)
        results = self._model.predict_batch(chunks)
        return _aggregate_chunks(results)

    def analyse_batch(self, texts: list[str]) -> list[ReviewSentiment]:
        self.ensure_loaded()
        # Flatten all chunks with back-references
        all_chunks: list[str] = []
        chunk_map: list[tuple[int, int]] = []  # (review_idx, chunk_idx)
        per_review_chunks: list[list[str]] = []

        for text in texts:
            chunks = chunk_text(text, max_tokens=480)
            per_review_chunks.append(chunks)
            start = len(all_chunks)
            all_chunks.extend(chunks)

        if not all_chunks:
            return []

        flat_results = self._model.predict_batch(all_chunks)

        # Reassemble
        results: list[ReviewSentiment] = []
        idx = 0
        for chunks in per_review_chunks:
            chunk_results = flat_results[idx: idx + len(chunks)]
            results.append(_aggregate_chunks(chunk_results))
            idx += len(chunks)

        return results