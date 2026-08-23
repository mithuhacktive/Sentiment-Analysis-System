from __future__ import annotations
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        protected_namespaces=("settings_",),
    )

    # Core
    sentiguard_env: str = "development"
    sentiguard_debug: bool = False
    sentiguard_offline: bool = False

    # Database
    database_url: str = "sqlite+aiosqlite:///./sentiguard.db"

    # Model
    sentiment_model: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    model_device: str = "cpu"
    model_batch_size: int = 16
    model_max_length: int = 512

    # Retrieval budget
    max_sources: int = 8
    max_reviews_per_source: int = 50
    max_total_reviews: int = 250
    request_timeout_seconds: int = 20

    # Cache
    cache_ttl_seconds: int = 3600
    cache_max_size: int = 512

    # Optional external APIs
    serpapi_api_key: str = ""
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_user_agent: str = "sentiguard/1.0"

    # Thresholds
    min_reviews_for_conclusion: int = 3
    duplicate_similarity_threshold: float = 0.85
    spam_score_threshold: float = 0.7
    low_confidence_threshold: float = 0.55
    high_confidence_threshold: float = 0.80

    # Evidence weights
    weight_source_quality: float = 0.25
    weight_review_quality: float = 0.20
    weight_freshness: float = 0.15
    weight_sentiment_strength: float = 0.20
    weight_product_match: float = 0.10
    weight_language_confidence: float = 0.10

    @property
    def has_serpapi(self) -> bool:
        return bool(self.serpapi_api_key)

    @property
    def has_reddit(self) -> bool:
        return bool(self.reddit_client_id and self.reddit_client_secret)


@lru_cache
def get_settings() -> Settings:
    return Settings()