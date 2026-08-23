from __future__ import annotations
import re
import logging
from dataclasses import dataclass
from app.utils.hashing import content_hash

logger = logging.getLogger(__name__)

# Common brand signals
_KNOWN_BRANDS = {
    "sony", "samsung", "apple", "google", "oneplus", "xiaomi", "realme", "oppo",
    "vivo", "nokia", "motorola", "lg", "huawei", "asus", "lenovo", "dell",
    "hp", "acer", "bose", "jbl", "sennheiser", "philips", "anker",
}

_CONVERSATIONAL_STRIP = re.compile(
    r"^(analyze|analyse|what (are|do) (people|users|customers) (say|think|feel) about|"
    r"review|tell me about|give me (the )?sentiment for|check|look up)\s+",
    re.IGNORECASE,
)


@dataclass
class ResolvedProduct:
    product_id: str
    canonical_name: str
    brand: str | None
    model: str | None
    variant: str | None
    region: str | None
    confidence: float
    status: str  # RESOLVED | AMBIGUOUS | NOT_FOUND


def _strip_conversational(query: str) -> str:
    return _CONVERSATIONAL_STRIP.sub("", query).strip()


def _extract_brand(text: str) -> str | None:
    words = text.lower().split()
    for word in words:
        if word in _KNOWN_BRANDS:
            return word.title()
    return None


def resolve_product(
    query: str,
    brand: str | None = None,
    model_hint: str | None = None,
    region: str | None = None,
    url: str | None = None,
) -> ResolvedProduct:
    """
    Deterministic product resolver.
    No LLM required. Returns structured product identity.
    """
    cleaned = _strip_conversational(query)

    # Remove URL if embedded
    if url:
        cleaned = cleaned.replace(url, "").strip()

    # Extract brand
    detected_brand = brand or _extract_brand(cleaned)

    # Canonical name is the cleaned query (title-cased)
    canonical = cleaned.strip()
    if not canonical:
        return ResolvedProduct(
            product_id="unknown",
            canonical_name="Unknown",
            brand=None,
            model=None,
            variant=None,
            region=region,
            confidence=0.0,
            status="NOT_FOUND",
        )

    # Ambiguity detection: very short names without brand
    words = canonical.split()
    if len(words) == 1 and not detected_brand:
        status = "AMBIGUOUS"
        confidence = 0.45
    elif len(words) <= 2 and not detected_brand:
        status = "AMBIGUOUS"
        confidence = 0.60
    else:
        status = "RESOLVED"
        confidence = 0.85 if detected_brand else 0.70

    # URL gives extra confidence
    if url:
        confidence = min(confidence + 0.10, 0.97)

    product_id = content_hash(canonical.lower())[:24]

    return ResolvedProduct(
        product_id=product_id,
        canonical_name=canonical,
        brand=detected_brand,
        model=model_hint,
        variant=None,
        region=region or "GLOBAL",
        confidence=round(confidence, 3),
        status=status,
    )