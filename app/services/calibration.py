from __future__ import annotations
import logging
from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


def calibrate_confidence(raw_probability: float, label: str, n_reviews: int) -> float:
    """
    Post-hoc calibration with sample-size penalty.
    Penalty is mild — we have real evidence, just flag uncertainty.
    Floor 0.05, ceiling 0.98.
    """
    if n_reviews < 3:
        factor = 0.65
    elif n_reviews < 5:
        factor = 0.75
    elif n_reviews < 15:
        factor = 0.88
    elif n_reviews < 30:
        factor = 0.95
    else:
        factor = 1.0

    calibrated = raw_probability * factor
    calibrated = max(0.05, min(0.98, calibrated))
    return round(calibrated, 4)


def confidence_label(confidence: float) -> str:
    if confidence >= settings.high_confidence_threshold:
        return "HIGH"
    elif confidence >= settings.low_confidence_threshold:
        return "MODERATE"
    else:
        return "LOW"
