from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class RawReview:
    source: str
    source_url: str
    external_id: str | None
    review_text: str
    rating: float | None
    review_date: datetime | None
    author: str | None
    retrieval_method: str  # API | SCRAPE | FIXTURE | SEARCH


@dataclass
class AdapterResult:
    source: str
    url: str
    reviews: list[RawReview] = field(default_factory=list)
    success: bool = True
    error: str | None = None
    discovery_method: str = "unknown"
    retrieved_at: datetime = field(default_factory=datetime.utcnow)


class BaseAdapter(ABC):
    name: str = "base"

    @abstractmethod
    async def fetch(self, query: str, product_url: str | None = None) -> AdapterResult:
        ...

    def is_available(self) -> bool:
        return True