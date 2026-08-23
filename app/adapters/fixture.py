from __future__ import annotations
import json
import logging
from datetime import datetime
from pathlib import Path
from app.adapters.base import BaseAdapter, AdapterResult, RawReview

logger = logging.getLogger(__name__)

FIXTURE_PATH = Path(__file__).parent.parent.parent / "tests" / "fixtures" / "reviews.json"


class FixtureAdapter(BaseAdapter):
    name = "fixture"

    def is_available(self) -> bool:
        return FIXTURE_PATH.exists()

    async def fetch(self, query: str, product_url: str | None = None) -> AdapterResult:
        if not FIXTURE_PATH.exists():
            return AdapterResult(
                source=self.name,
                url="fixture://local",
                success=False,
                error="Fixture file not found",
            )

        try:
            data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
            reviews: list[RawReview] = []

            for item in data.get("reviews", []):
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

            logger.info("FixtureAdapter loaded %d reviews", len(reviews))
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