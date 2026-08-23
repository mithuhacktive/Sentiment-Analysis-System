from __future__ import annotations
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

try:
    from langdetect import detect_langs, LangDetectException
    _LANGDETECT_AVAILABLE = True
except ImportError:
    _LANGDETECT_AVAILABLE = False
    logger.warning("langdetect not available; language detection disabled")

SUPPORTED_LANGUAGES = {"en"}  # Model supports multilingual but we track this
MIN_CONFIDENCE = 0.70


@dataclass
class LanguageResult:
    language: str
    confidence: float
    status: str  # DETECTED | LANGUAGE_UNCERTAIN | UNSUPPORTED_LANGUAGE | DETECTION_FAILED


def detect_language(text: str) -> LanguageResult:
    if not _LANGDETECT_AVAILABLE:
        return LanguageResult("en", 1.0, "DETECTED")  # assume English fallback

    if len(text.strip()) < 10:
        return LanguageResult("unknown", 0.0, "LANGUAGE_UNCERTAIN")

    try:
        langs = detect_langs(text)
        top = langs[0]
        lang = top.lang
        conf = float(top.prob)

        if conf < MIN_CONFIDENCE:
            return LanguageResult(lang, conf, "LANGUAGE_UNCERTAIN")

        return LanguageResult(lang, conf, "DETECTED")

    except Exception as e:
        logger.debug("Language detection failed: %s", e)
        return LanguageResult("unknown", 0.0, "DETECTION_FAILED")