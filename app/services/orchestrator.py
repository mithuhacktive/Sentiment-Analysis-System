from __future__ import annotations
import asyncio
import json
import logging
import uuid
from datetime import datetime, timezone
from app.adapters.base import RawReview
from app.adapters.fixture import FixtureAdapter
from app.adapters.url import URLAdapter
from app.adapters.serpapi import SerpApiAdapter
from app.adapters.reddit import RedditAdapter
from app.config import get_settings
from app.services.product_resolver import resolve_product
from app.services.normalization import normalise_review
from app.services.language import detect_language
from app.services.duplicates import DuplicateDetector, ReviewForDedup
from app.services.quality import ReviewQualityScorer
from app.services.sentiment import SentimentService
from app.services.aspects import AspectAnalyser
from app.services.evidence import score_evidence
from app.services.aggregation import aggregate
from app.utils.hashing import author_hash
from app.utils.timing import timer
from app.utils.urls import is_valid_url

logger = logging.getLogger(__name__)
settings = get_settings()


class Orchestrator:
    def __init__(self) -> None:
        self._sentiment = SentimentService()
        self._aspect = AspectAnalyser()
        self._dedup = DuplicateDetector()
        self._quality = ReviewQualityScorer()
        self._adapters = [
            FixtureAdapter() if settings.sentiguard_offline else None,
            URLAdapter(),
            SerpApiAdapter(),
            RedditAdapter(),
        ]
        self._adapters = [a for a in self._adapters if a is not None]

        if settings.sentiguard_offline:
            self._adapters = [FixtureAdapter()]

    async def analyse(self, query: str, fresh: bool = False, region: str | None = None) -> dict:
        analysis_id = str(uuid.uuid4())
        started_at = datetime.now(timezone.utc)

        with timer("total") as t_total:
            # 1. Detect if query is URL
            product_url: str | None = None
            clean_query = query.strip()
            if is_valid_url(clean_query):
                product_url = clean_query

            # 2. Resolve product
            with timer("resolve") as t_resolve:
                product = resolve_product(
                    query=clean_query,
                    region=region,
                    url=product_url,
                )

            limitations: list[str] = []

            if product.status == "AMBIGUOUS":
                limitations.append(f"Product identity is ambiguous for query: '{clean_query}'")
            if product.status == "NOT_FOUND":
                return self._build_response(
                    analysis_id=analysis_id,
                    status="FAILED",
                    query=query,
                    product=product,
                    limitations=["Product could not be identified from the query."],
                    started_at=started_at,
                    t_total=0,
                )

            # 3. Retrieve from all adapters concurrently
            with timer("retrieval") as t_retrieval:
                adapter_tasks = [
                    a.fetch(clean_query, product_url)
                    for a in self._adapters
                    if a.is_available()
                ]
                adapter_results = await asyncio.gather(*adapter_tasks, return_exceptions=True)

            sources_attempted = len(adapter_tasks)
            sources_successful = 0
            all_raw_reviews: list[RawReview] = []

            for result in adapter_results:
                if isinstance(result, Exception):
                    logger.warning("Adapter raised exception: %s", result)
                    continue
                if result.success:
                    sources_successful += 1
                    all_raw_reviews.extend(result.reviews)
                else:
                    limitations.append(f"Source '{result.source}' failed: {result.error}")

            # Cap total reviews
            all_raw_reviews = all_raw_reviews[:settings.max_total_reviews]

            if not all_raw_reviews:
                return self._build_response(
                    analysis_id=analysis_id,
                    status="INSUFFICIENT_EVIDENCE",
                    query=query,
                    product=product,
                    limitations=limitations + ["No reviews could be retrieved."],
                    started_at=started_at,
                    t_total=t_total["ms"],
                )

            # 4. Normalise
            with timer("normalise") as t_norm:
                for rev in all_raw_reviews:
                    norm = normalise_review(rev.review_text)
                    rev._norm = norm

            # 5. Language detection + dedup input
            dedup_inputs: list[ReviewForDedup] = []
            for i, rev in enumerate(all_raw_reviews):
                norm = rev._norm
                dedup_inputs.append(ReviewForDedup(
                    review_id=f"r{i}",
                    content_hash=norm["content_hash"],
                    normalised_hash=norm["normalised_hash"],
                    text=norm["normalized_text"],
                ))

            # 6. Dedup
            dedup_results = self._dedup.detect(dedup_inputs)
            dedup_map = {r.review_id: r for r in dedup_results}

            # 7. Sentiment (batch, all reviews)
            with timer("sentiment") as t_sent:
                texts = [rev._norm["normalized_text"] for rev in all_raw_reviews]
                try:
                    sentiments = self._sentiment.analyse_batch(texts)
                except Exception as e:
                    logger.error("Sentiment batch failed: %s", e)
                    return self._build_response(
                        analysis_id=analysis_id,
                        status="FAILED",
                        query=query,
                        product=product,
                        limitations=limitations + [f"Sentiment model error: {e}"],
                        started_at=started_at,
                        t_total=t_total["ms"],
                    )

            # 8. Quality scoring + evidence scoring
            enriched: list[dict] = []
            duplicates_found = 0
            suspicious_count = 0

            for i, rev in enumerate(all_raw_reviews):
                rid = f"r{i}"
                dedup = dedup_map.get(rid)
                dup_status = dedup.status if dedup else "ORIGINAL"

                if dup_status != "ORIGINAL":
                    duplicates_found += 1

                sent = sentiments[i]
                lang_result = detect_language(rev._norm["normalized_text"])

                quality = self._quality.score(
                    text=rev._norm["normalized_text"],
                    duplicate_status=dup_status,
                    rating=rev.rating,
                    sentiment_label=sent.label,
                )

                if quality.label == "SUSPICIOUS":
                    suspicious_count += 1

                evidence = score_evidence(
                    review_id=rid,
                    source=rev.source,
                    quality_score=quality.score,
                    language_confidence=lang_result.confidence,
                    duplicate_status=dup_status,
                    product_match_confidence=product.confidence,
                    review_date=rev.review_date,
                    sentiment_confidence=sent.confidence,
                )

                enriched.append({
                    "id": rid,
                    "label": sent.label,
                    "probabilities": sent.probabilities,
                    "evidence_score": evidence.score,
                    "source": rev.source,
                    "duplicate_status": dup_status,
                    "quality_label": quality.label,
                })

            # 9. Aspect analysis
            with timer("aspects") as t_asp:
                try:
                    aspect_results = self._aspect.analyse(texts[:100])  # cap for speed
                except Exception as e:
                    logger.warning("Aspect analysis failed: %s", e)
                    aspect_results = []

            # 10. Aggregate
            with timer("aggregate") as t_agg:
                n_independent = sum(1 for r in enriched if r["duplicate_status"] == "ORIGINAL")
                agg = aggregate(
                    reviews=enriched,
                    product_match_confidence=product.confidence,
                    n_independent=n_independent,
                )

            # 11. Build source summary
            source_map: dict[str, list[dict]] = {}
            for r in enriched:
                source_map.setdefault(r["source"], []).append(r)

            source_infos = []
            for src, items in source_map.items():
                dist: dict[str, float] = {}
                for lbl in ("POSITIVE", "NEGATIVE", "NEUTRAL"):
                    dist[lbl] = round(sum(1 for x in items if x["label"] == lbl) / len(items), 3)
                source_infos.append({
                    "source": src,
                    "review_count": len(items),
                    "sentiment_distribution": dist,
                })

            if agg.abstain:
                status = "INSUFFICIENT_EVIDENCE"
                if agg.abstain_reason:
                    limitations.append(f"Abstaining: {agg.abstain_reason}")
            else:
                status = "COMPLETED"

        return self._build_response(
            analysis_id=analysis_id,
            status=status,
            query=query,
            product=product,
            agg=agg,
            aspect_results=aspect_results,
            enriched=enriched,
            source_infos=source_infos,
            duplicates_found=duplicates_found,
            suspicious_count=suspicious_count,
            sources_attempted=sources_attempted,
            sources_successful=sources_successful,
            limitations=limitations,
            started_at=started_at,
            t_total=t_total["ms"],
        )

    def _build_response(
        self,
        analysis_id: str,
        status: str,
        query: str,
        product=None,
        agg=None,
        aspect_results=None,
        enriched=None,
        source_infos=None,
        duplicates_found: int = 0,
        suspicious_count: int = 0,
        sources_attempted: int = 0,
        sources_successful: int = 0,
        limitations=None,
        started_at=None,
        t_total: float = 0.0,
    ) -> dict:
        now = datetime.now(timezone.utc)
        product_info = None
        if product:
            product_info = {
                "name": product.canonical_name,
                "brand": product.brand,
                "model": product.model,
                "variant": product.variant,
                "region": product.region,
                "confidence": product.confidence,
                "resolution_status": product.status,
            }

        overall = None
        if agg and not agg.abstain:
            overall = {
                "label": agg.label,
                "confidence": agg.calibrated_confidence,
                "calibrated": True,
            }

        aspects = []
        if aspect_results:
            for a in aspect_results:
                aspects.append({
                    "name": a.name,
                    "label": a.label,
                    "confidence": a.confidence,
                    "evidence_count": a.evidence_count,
                })

        evidence = None
        if enriched is not None:
            evidence = {
                "reviews_analyzed": len(enriched),
                "independent_reviews": sum(1 for r in enriched if r["duplicate_status"] == "ORIGINAL"),
                "sources": sources_successful,
                "duplicates": duplicates_found,
                "suspicious_reviews": suspicious_count,
                "conflict_level": agg.conflict_level if agg else "LOW",
            }

        return {
            "analysis_id": analysis_id,
            "status": status,
            "product": product_info,
            "overall": overall,
            "aspects": aspects,
            "evidence": evidence,
            "sources": source_infos or [],
            "limitations": limitations or [],
            "pipeline": {
                "version": "1.0.0",
                "model": settings.sentiment_model,
                "retrieved_at": (started_at or now).isoformat(),
                "processing_time_ms": t_total,
                "cache_used": False,
                "data_freshness": "LIVE",
            },
        }