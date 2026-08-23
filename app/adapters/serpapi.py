from __future__ import annotations
import logging
from datetime import datetime
from app.adapters.base import BaseAdapter, AdapterResult, RawReview
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

try:
    import httpx
    _HTTPX_OK = True
except ImportError:
    _HTTPX_OK = False

SERPAPI_URL = "https://serpapi.com/search"


class SerpApiAdapter(BaseAdapter):
    name = "serpapi"

    def is_available(self) -> bool:
        return bool(settings.serpapi_api_key) and _HTTPX_OK and not settings.sentiguard_offline

    async def fetch(self, query: str, product_url: str | None = None) -> AdapterResult:
        if not self.is_available():
            return AdapterResult(
                source=self.name,
                url=SERPAPI_URL,
                success=False,
                error="SERPAPI_NOT_CONFIGURED",
            )

        search_queries = [
            f"{query} reviews",
            f"{query} user review problems",
        ]

        all_reviews: list[RawReview] = []

        try:
            async with httpx.AsyncClient(timeout=15) as client:
                for sq in search_queries:
                    params = {
                        "q": sq,
                        "api_key": settings.serpapi_api_key,
                        "engine": "google",
                        "num": 10,
                    }
                    try:
                        resp = await client.get(SERPAPI_URL, params=params)
                        if resp.status_code != 200:
                            logger.warning("SerpAPI returned %d for query: %s", resp.status_code, sq)
                            continue

                        data = resp.json()
                        organic = data.get("organic_results", [])

                        for item in organic:
                            snippet = item.get("snippet", "")
                            title = item.get("title", "")
                            link = item.get("link", "")

                            # Snippets are NOT treated as reviews — they are discovery signals only
                            # We log them but do not include as review evidence
                            logger.debug("SerpAPI discovered: %s — %s", title, link)

                    except Exception as e:
                        logger.warning("SerpAPI query failed: %s — %s", sq, e)
                        continue

        except Exception as e:
            return AdapterResult(
                source=self.name,
                url=SERPAPI_URL,
                success=False,
                error=str(e),
            )

        # SerpAPI used for discovery only in this implementation
        # Real review text comes from URLAdapter after discovery
        return AdapterResult(
            source=self.name,
            url=SERPAPI_URL,
            reviews=all_reviews,
            success=True,
            discovery_method="SEARCH_API",
        )