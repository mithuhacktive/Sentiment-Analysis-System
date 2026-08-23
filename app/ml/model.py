from __future__ import annotations
import logging
from dataclasses import dataclass
from typing import Optional
import numpy as np
from transformers import pipeline, Pipeline
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_LABEL_MAP = {
    # cardiffnlp labels
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "NEUTRAL",
    "LABEL_2": "POSITIVE",
    # some versions use these directly
    "negative": "NEGATIVE",
    "neutral": "NEUTRAL",
    "positive": "POSITIVE",
    "NEGATIVE": "NEGATIVE",
    "NEUTRAL": "NEUTRAL",
    "POSITIVE": "POSITIVE",
}


@dataclass
class SentimentResult:
    label: str
    probabilities: dict[str, float]
    raw_score: float


class SentimentModel:
    def __init__(self) -> None:
        self._pipeline: Optional[Pipeline] = None
        self._loaded = False

    def load(self) -> None:
        if self._loaded:
            return
        try:
            logger.info("Loading sentiment model: %s", settings.sentiment_model)
            self._pipeline = pipeline(
                "text-classification",
                model=settings.sentiment_model,
                top_k=None,  # return all class scores
                device=-1,   # CPU
                truncation=True,
                max_length=settings.model_max_length,
            )
            self._loaded = True
            logger.info("Sentiment model loaded successfully")
        except Exception as e:
            logger.error("Failed to load model: %s", e)
            self._loaded = False
            raise

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    def _normalise_output(self, raw: list[dict]) -> SentimentResult:
        probs: dict[str, float] = {}
        for item in raw:
            label = _LABEL_MAP.get(item["label"], item["label"].upper())
            probs[label] = float(item["score"])
        # Ensure all three classes present
        for cls in ("POSITIVE", "NEGATIVE", "NEUTRAL"):
            probs.setdefault(cls, 0.0)
        predicted = max(probs, key=lambda k: probs[k])
        return SentimentResult(
            label=predicted,
            probabilities=probs,
            raw_score=probs[predicted],
        )

    def predict(self, text: str) -> SentimentResult:
        if not self._loaded or self._pipeline is None:
            raise RuntimeError("Model not loaded")
        result = self._pipeline(text, truncation=True, max_length=settings.model_max_length)
        return self._normalise_output(result)

    def predict_batch(self, texts: list[str]) -> list[SentimentResult]:
        if not self._loaded or self._pipeline is None:
            raise RuntimeError("Model not loaded")
        if not texts:
            return []
        results = self._pipeline(
            texts,
            truncation=True,
            max_length=settings.model_max_length,
            batch_size=settings.model_batch_size,
        )
        return [self._normalise_output(r) for r in results]


# Singleton
_model_instance: Optional[SentimentModel] = None


def get_model() -> SentimentModel:
    global _model_instance
    if _model_instance is None:
        _model_instance = SentimentModel()
    return _model_instance