from __future__ import annotations
import logging
from dataclasses import dataclass
from app.config import get_settings
from app.services.calibration import calibrate_confidence

settings = get_settings()
logger = logging.getLogger(__name__)


@dataclass
class AggregatedResult:
    label: str
    raw_confidence: float
    calibrated_confidence: float
    conflict_level: str
    source_distribution: dict[str, dict[str, float]]
    abstain: bool
    abstain_reason: str | None


def compute_conflict(source_dist: dict[str, dict[str, float]]) -> tuple[str, float]:
    if len(source_dist) < 2:
        return "LOW", 0.0

    dominant_labels = []
    for dist in source_dist.values():
        dominant = max(dist, key=lambda k: dist[k])
        dominant_labels.append(dominant)

    unique = set(dominant_labels)
    if len(unique) == 1:
        return "LOW", 0.0
    elif len(unique) == 2:
        minority = min(dominant_labels.count(l) for l in unique)
        ratio = minority / len(dominant_labels)
        if ratio <= 0.25:
            return "LOW", ratio
        elif ratio <= 0.45:
            return "MODERATE", ratio
        else:
            return "HIGH", ratio
    else:
        return "HIGH", 1.0


def aggregate(
    reviews: list[dict],
    product_match_confidence: float,
    n_independent: int,
) -> AggregatedResult:
    if not reviews:
        return AggregatedResult(
            label="INSUFFICIENT_EVIDENCE",
            raw_confidence=0.0,
            calibrated_confidence=0.0,
            conflict_level="LOW",
            source_distribution={},
            abstain=True,
            abstain_reason="NO_REVIEWS",
        )

    total_weight = 0.0
    weighted_probs: dict[str, float] = {"POSITIVE": 0.0, "NEGATIVE": 0.0, "NEUTRAL": 0.0}
    source_sentiments: dict[str, list[str]] = {}

    for r in reviews:
        w = r.get("evidence_score", 0.5)
        probs = r.get("probabilities", {})
        total_weight += w
        for cls in weighted_probs:
            weighted_probs[cls] += w * probs.get(cls, 0.0)
        src = r.get("source", "unknown")
        source_sentiments.setdefault(src, []).append(r.get("label", "NEUTRAL"))

    if total_weight == 0:
        return AggregatedResult(
            label="INSUFFICIENT_EVIDENCE",
            raw_confidence=0.0,
            calibrated_confidence=0.0,
            conflict_level="LOW",
            source_distribution={},
            abstain=True,
            abstain_reason="ZERO_WEIGHT",
        )

    for cls in weighted_probs:
        weighted_probs[cls] /= total_weight

    label = max(weighted_probs, key=lambda k: weighted_probs[k])
    raw_conf = weighted_probs[label]

    # Source distribution per source
    source_dist: dict[str, dict[str, float]] = {}
    for src, labels in source_sentiments.items():
        dist: dict[str, float] = {}
        for lbl in ("POSITIVE", "NEGATIVE", "NEUTRAL"):
            dist[lbl] = round(labels.count(lbl) / len(labels), 3)
        source_dist[src] = dist

    conflict_level, conflict_score = compute_conflict(source_dist)

    # Conflict penalty — minimal, conflict is reported honestly in output
    # Real-world cross-platform sentiment always conflicts (Reddit vs Amazon)
    if conflict_level == "HIGH":
        raw_conf *= 0.95
    elif conflict_level == "MODERATE":
        raw_conf *= 0.98

    calibrated = calibrate_confidence(raw_conf, label, n_independent)

    logger.debug(
        "Aggregation: label=%s raw=%.4f calibrated=%.4f conflict=%s n=%d",
        label, raw_conf, calibrated, conflict_level, n_independent,
    )

    # Abstention — only truly unresolvable cases
    abstain = False
    abstain_reason = None

    if n_independent < settings.min_reviews_for_conclusion:
        abstain = True
        abstain_reason = "INSUFFICIENT_REVIEWS"
    elif calibrated < 0.30:
        # Near-random confidence — no useful signal
        abstain = True
        abstain_reason = "LOW_CONFIDENCE"
    elif product_match_confidence < 0.40:
        abstain = True
        abstain_reason = "PRODUCT_MATCH_UNCERTAIN"

    return AggregatedResult(
        label=label if not abstain else "INSUFFICIENT_EVIDENCE",
        raw_confidence=round(raw_conf, 4),
        calibrated_confidence=round(calibrated, 4),
        conflict_level=conflict_level,
        source_distribution=source_dist,
        abstain=abstain,
        abstain_reason=abstain_reason,
    )