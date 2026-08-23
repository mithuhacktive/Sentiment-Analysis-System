from __future__ import annotations
import math
import logging
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


def calibrate_confidence(raw_probability: float, label: str, n_reviews: int) -> float:
    """
    Simple post-hoc calibration:
    1. Apply slight regression-to-mean for small sample sizes.
    2. Penalise very small review counts.
    Proper Platt scaling / temperature scaling requires a held-out cal set.
    """
    # Small-sample penalty
    if n_reviews < 5:
        factor = 0.7
    elif n_reviews < 15:
        factor = 0.85
    elif n_reviews < 30:
        factor = 0.93
    else:
        factor = 1.0

    calibrated = raw_probability * factor

    # Soft floor / ceiling
    calibrated = max(0.05, min(0.98, calibrated))
    return round(calibrated, 4)


def confidence_label(confidence: float) -> str:
    if confidence >= settings.high_confidence_threshold:
        return "HIGH"
    elif confidence >= settings.low_confidence_threshold:
        return "MODERATE"
    else:
        return "LOW"