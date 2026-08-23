from __future__ import annotations
import logging
from datetime import datetime, timezone
from app.adapters.base import BaseAdapter, AdapterResult, RawReview
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

try:
    import httpx
    _HTTPX_OK = True
except ImportError:
    _HTTPX_OK = False

REDDIT_SEARCH_URL = "https://www.reddit.com/search.json"
SUBREDDITS = ["reviews", "BuyItForLife", "hardware", "gadgets", "headphones", "audiophile"]


class RedditAdapter(BaseAdapter):
    name = "reddit"

    def is_available(self) -> bool:
        return _HTTPX_OK and not settings.sentiguard_offline

    async def fetch(self, query: str, product_url: str | None = None) -> AdapterResult:
        if not self.is_available():
            return AdapterResult(
                source=self.name,
                url=REDDIT_SEARCH_URL,
                success=False,
                error="REDDIT_UNAVAILABLE",
            )

        reviews: list[RawReview] = []
        headers = {"User-Agent": settings.reddit_user_agent}

        try:
            async with httpx.AsyncClient(timeout=15, headers=headers) as client:
                params = {
                    "q": query,
                    "type": "link",
                    "sort": "relevance",
                    "limit": 25,
                    "t": "year",
                }
                resp = await client.get(REDDIT_SEARCH_URL, params=params)

                if resp.status_code == 429:
                    return AdapterResult(
                        source=self.name,
                        url=REDDIT_SEARCH_URL,
                        success=False,
                        error="RATE_LIMITED",
                    )

                if resp.status_code != 200:
                    return AdapterResult(
                        source=self.name,
                        url=REDDIT_SEARCH_URL,
                        success=False,
                        error=f"HTTP_{resp.status_code}",
                    )

                data = resp.json()
                posts = data.get("data", {}).get("children", [])

                for i, post in enumerate(posts[:settings.max_reviews_per_source]):
                    post_data = post.get("data", {})
                    selftext = post_data.get("selftext", "").strip()
                    title = post_data.get("title", "").strip()

                    # Combine title + body for review text
                    combined = f"{title}. {selftext}".strip(" .")
                    if len(combined.split()) < 5:
                        continue

                    created = post_data.get("created_utc")
                    review_date = (
                        datetime.fromtimestamp(created, tz=timezone.utc) if created else None
                    )

                    score = post_data.get("score", 0)
                    # Normalise Reddit score as a proxy for quality (not used as rating)

                    reviews.append(RawReview(
                        source="reddit",
                        source_url=f"https://reddit.com{post_data.get('permalink', '')}",
                        external_id=post_data.get("id"),
                        review_text=combined[:3000],
                        rating=None,  # Reddit has no star rating
                        review_date=review_date,
                        author=post_data.get("author"),
                        retrieval_method="API",
                    ))

        except httpx.TimeoutException:
            return AdapterResult(
                source=self.name,
                url=REDDIT_SEARCH_URL,
                success=False,
                error="TIMEOUT",
            )
        except Exception as e:
            logger.warning("RedditAdapter error: %s", e)
            return AdapterResult(
                source=self.name,
                url=REDDIT_SEARCH_URL,
                success=False,
                error=str(e),
            )

        logger.info("RedditAdapter retrieved %d posts", len(reviews))
        return AdapterResult(
            source=self.name,
            url=REDDIT_SEARCH_URL,
            reviews=reviews,
            success=True,
            discovery_method="REDDIT_SEARCH",
        )