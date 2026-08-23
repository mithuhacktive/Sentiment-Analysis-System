from __future__ import annotations
import logging
import re
from datetime import datetime
from app.adapters.base import BaseAdapter, AdapterResult, RawReview
from app.utils.urls import is_valid_url, is_safe_url
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

try:
    import httpx
    from bs4 import BeautifulSoup
    _DEPS_OK = True
except ImportError:
    _DEPS_OK = False
    logger.warning("httpx or beautifulsoup4 not available; URLAdapter disabled")

MAX_RESPONSE_BYTES = 5 * 1024 * 1024  # 5 MB
MAX_REDIRECTS = 5
ALLOWED_CONTENT_TYPES = {"text/html", "application/xhtml+xml"}

PAGE_OUTCOMES = {
    200: "PRODUCT_PAGE",
    301: "REDIRECT",
    302: "REDIRECT",
    403: "BLOCKED_PAGE",
    404: "EMPTY_PAGE",
    429: "RATE_LIMITED",
    500: "SERVER_ERROR",
}


def _classify_page(soup: "BeautifulSoup", url: str) -> str:
    text = soup.get_text(separator=" ", strip=True).lower()
    if any(kw in text for kw in ["sign in", "log in", "login required", "please log in"]):
        return "LOGIN_PAGE"
    if any(kw in text for kw in ["captcha", "robot", "unusual traffic"]):
        return "BLOCKED_PAGE"
    if any(kw in text for kw in ["search results", "results for", "showing results"]):
        return "SEARCH_PAGE"
    return "PRODUCT_PAGE"


def _extract_reviews(soup: "BeautifulSoup", source_url: str) -> list[RawReview]:
    reviews: list[RawReview] = []

    # Generic heuristic: look for review-like containers
    candidates = soup.find_all(
        attrs={"class": re.compile(r"review|comment|feedback|testimonial", re.I)}
    )

    for i, tag in enumerate(candidates[:50]):
        text = tag.get_text(separator=" ", strip=True)
        if len(text.split()) < 5:
            continue

        # Try to extract rating
        rating = None
        rating_tag = tag.find(attrs={"class": re.compile(r"rating|star|score", re.I)})
        if rating_tag:
            nums = re.findall(r"\b([1-5](?:\.\d)?)\b", rating_tag.get_text())
            if nums:
                try:
                    rating = float(nums[0])
                except ValueError:
                    pass

        reviews.append(RawReview(
            source="generic_url",
            source_url=source_url,
            external_id=f"url_{i}",
            review_text=text[:3000],
            rating=rating,
            review_date=None,
            author=None,
            retrieval_method="SCRAPE",
        ))

    return reviews


class URLAdapter(BaseAdapter):
    name = "url"

    def is_available(self) -> bool:
        return _DEPS_OK

    async def fetch(self, query: str, product_url: str | None = None) -> AdapterResult:
        url = product_url or query

        if not _DEPS_OK:
            return AdapterResult(source=self.name, url=url, success=False, error="dependencies_missing")

        if not is_valid_url(url):
            return AdapterResult(source=self.name, url=url, success=False, error="INVALID_URL")

        safe, reason = is_safe_url(url)
        if not safe:
            return AdapterResult(source=self.name, url=url, success=False, error=f"UNSAFE_URL:{reason}")

        try:
            async with httpx.AsyncClient(
                timeout=settings.request_timeout_seconds,
                max_redirects=MAX_REDIRECTS,
                follow_redirects=True,
                headers={"User-Agent": "SentiGuard/1.0 (research; not scraping)"},
            ) as client:
                resp = await client.get(url)

            status = resp.status_code
            if status != 200:
                return AdapterResult(
                    source=self.name,
                    url=url,
                    success=False,
                    error=PAGE_OUTCOMES.get(status, f"HTTP_{status}"),
                )

            content_type = resp.headers.get("content-type", "").split(";")[0].strip()
            if content_type not in ALLOWED_CONTENT_TYPES:
                return AdapterResult(
                    source=self.name,
                    url=url,
                    success=False,
                    error=f"UNSUPPORTED_CONTENT_TYPE:{content_type}",
                )

            if len(resp.content) > MAX_RESPONSE_BYTES:
                return AdapterResult(source=self.name, url=url, success=False, error="RESPONSE_TOO_LARGE")

            soup = BeautifulSoup(resp.text, "lxml")
            page_type = _classify_page(soup, url)

            if page_type in ("LOGIN_PAGE", "BLOCKED_PAGE"):
                return AdapterResult(source=self.name, url=url, success=False, error=page_type)

            reviews = _extract_reviews(soup, url)

            return AdapterResult(
                source=self.name,
                url=url,
                reviews=reviews,
                success=True,
                discovery_method="USER_URL",
            )

        except httpx.TimeoutException:
            return AdapterResult(source=self.name, url=url, success=False, error="TIMEOUT")
        except Exception as e:
            logger.warning("URLAdapter error for %s: %s", url, e)
            return AdapterResult(source=self.name, url=url, success=False, error=str(e))