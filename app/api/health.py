from __future__ import annotations
import logging
from fastapi import APIRouter
from app.schemas.responses import HealthResponse
from app.ml.model import get_model
from app.config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    model = get_model()
    return HealthResponse(
        status="ok",
        version="1.0.0",
        model_loaded=model.is_loaded,
        database_ok=True,
        offline_mode=settings.sentiguard_offline,
    )


@router.get("/health/ready")
async def ready() -> dict:
    model = get_model()
    if not model.is_loaded:
        return {"ready": False, "reason": "model_not_loaded"}
    return {"ready": True}