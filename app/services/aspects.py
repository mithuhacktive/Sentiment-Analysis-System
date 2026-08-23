from __future__ import annotations
import re
import logging
from dataclasses import dataclass, field
from app.services.sentiment import SentimentService

logger = logging.getLogger(__name__)

# Aspect keyword dictionary — extend freely
ASPECT_KEYWORDS: dict[str, list[str]] = {
    "battery": ["battery", "battery life", "charge", "charging", "power", "mAh"],
    "performance": ["performance", "speed", "fast", "slow", "lag", "smooth", "responsive"],
    "build_quality": ["build", "quality", "sturdy", "durable", "flimsy", "cheap", "solid", "premium"],
    "display": ["display", "screen", "resolution", "brightness", "colour", "color", "refresh"],
    "camera": ["camera", "photo", "picture", "video", "lens", "megapixel", "selfie"],
    "comfort": ["comfort", "comfortable", "ergonomic", "fit", "wear", "cushion", "weight"],
    "sound": ["sound", "audio", "bass", "treble", "volume", "speaker", "headphone", "noise cancel"],
    "software": ["software", "app", "update", "bug", "interface", "UI", "firmware", "features"],
    "value": ["value", "price", "worth", "expensive", "cheap", "affordable", "cost", "money"],
    "shipping": ["shipping", "delivery", "packaging", "arrived", "damaged", "box"],
}


@dataclass
class AspectResult:
    name: str
    label: str
    confidence: float
    evidence_count: int
    evidence_snippets: list[str] = field(default_factory=list)


def _extract_aspect_sentences(text: str, keywords: list[str]) -> list[str]:
    sentences = re.split(r"[.!?;\n]", text)
    matched = []
    for s in sentences:
        s_lower = s.lower()
        if any(kw.lower() in s_lower for kw in keywords):
            stripped = s.strip()
            if stripped:
                matched.append(stripped)
    return matched


class AspectAnalyser:
    def __init__(self) -> None:
        self._sentiment = SentimentService()

    def analyse(self, reviews: list[str]) -> list[AspectResult]:
        results: list[AspectResult] = []

        for aspect_name, keywords in ASPECT_KEYWORDS.items():
            snippets: list[str] = []
            for review in reviews:
                snippets.extend(_extract_aspect_sentences(review, keywords))

            if not snippets:
                continue

            # Cap to avoid huge sentiment calls
            snippets = snippets[:60]

            try:
                sentiments = self._sentiment.analyse_batch(snippets)
            except Exception as e:
                logger.warning("Aspect sentiment failed for %s: %s", aspect_name, e)
                continue

            if not sentiments:
                continue

            # Average probabilities
            avg = {"POSITIVE": 0.0, "NEGATIVE": 0.0, "NEUTRAL": 0.0}
            for s in sentiments:
                for k, v in s.probabilities.items():
                    avg[k] = avg.get(k, 0.0) + v
            n = len(sentiments)
            for k in avg:
                avg[k] /= n

            label = max(avg, key=lambda x: avg[x])
            confidence = avg[label]

            results.append(AspectResult(
                name=aspect_name,
                label=label,
                confidence=round(confidence, 4),
                evidence_count=len(snippets),
                evidence_snippets=snippets[:3],
            ))

        return results