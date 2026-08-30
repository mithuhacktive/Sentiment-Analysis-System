from __future__ import annotations
import json
import logging
from datetime import datetime
from pathlib import Path
from app.adapters.base import BaseAdapter, AdapterResult, RawReview

logger = logging.getLogger(__name__)

FIXTURE_PATHS = [
    Path(__file__).parent.parent.parent / "tests" / "fixtures" / "reviews.json",
    Path(__file__).parent.parent.parent / "fixtures" / "reviews.json",
]


class FixtureAdapter(BaseAdapter):
    name = "fixture"

    def _get_existing_path(self) -> Path | None:
        for p in FIXTURE_PATHS:
            if p.exists():
                return p
        return None

    def is_available(self) -> bool:
        return self._get_existing_path() is not None

    async def fetch(self, query: str, product_url: str | None = None) -> AdapterResult:
        path = self._get_existing_path()
        if not path:
            logger.warning("FixtureAdapter: No fixture file found at paths: %s", FIXTURE_PATHS)
            return AdapterResult(
                source=self.name,
                url="fixture://local",
                success=False,
                error="Fixture file not found",
            )

        q_lower = (query or "").lower().strip()

        # Check if the query matches the product represented by the fixture file
        # tests/fixtures/reviews.json specifically contains Sony WH-1000XM5 / headphone reviews
        fixture_matches = any(
            kw in q_lower
            for kw in ["sony", "wh-1000xm5", "wh1000xm5", "1000xm5", "headphones", "headphone"]
        )

        if not fixture_matches:
            logger.info("FixtureAdapter: No fixture review dataset exists for query %r", query)
            return AdapterResult(
                source=self.name,
                url="fixture://local",
                reviews=[],
                success=False,
                error=f"NO_FIXTURE_REVIEWS_FOR_PRODUCT:{query}",
            )

        try:
            raw_content = path.read_text(encoding="utf-8")
            data = json.loads(raw_content)
            reviews: list[RawReview] = []

            items = data.get("reviews", []) if isinstance(data, dict) else data if isinstance(data, list) else []
            for item in items:
                reviews.append(RawReview(
                    source="fixture",
                    source_url=item.get("url", "fixture://local"),
                    external_id=item.get("id"),
                    review_text=item.get("text", ""),
                    rating=item.get("rating"),
                    review_date=datetime.fromisoformat(item["date"]) if item.get("date") else None,
                    author=item.get("author"),
                    retrieval_method="FIXTURE",
                ))

            logger.info("FixtureAdapter loaded %d reviews matching query %r", len(reviews), query)
            return AdapterResult(
                source=self.name,
                url="fixture://local",
                reviews=reviews,
                success=True,
                discovery_method="FIXTURE",
            )

        except Exception as e:
            logger.error("FixtureAdapter error: %s", e)
            return AdapterResult(
                source=self.name,
                url="fixture://local",
                success=False,
                error=str(e),
            )