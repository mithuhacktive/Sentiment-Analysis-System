from __future__ import annotations
import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.requests import AnalyzeRequest
from app.database import get_db
from app.services.orchestrator import Orchestrator
from app.config import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)
settings = get_settings()

_orchestrator: Orchestrator | None = None


def get_orchestrator() -> Orchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = Orchestrator()
    return _orchestrator


@router.post("/analyze")
async def analyze(
    request: AnalyzeRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    logger.info("Analyze request: query=%r fresh=%s", request.query, request.fresh)
    orch = get_orchestrator()
    try:
        result = await orch.analyse(
            query=request.query,
            fresh=request.fresh,
            region=request.region,
        )
        return result
    except Exception as e:
        logger.error("Analysis failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")


@router.get("/analyses/{analysis_id}")
async def get_analysis(analysis_id: str) -> dict:
    # Stub: full DB lookup would go here
    raise HTTPException(status_code=404, detail="Analysis not found (persistence stub)")
