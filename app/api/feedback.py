from __future__ import annotations
import logging
from fastapi import APIRouter
from app.schemas.requests import FeedbackRequest
from app.schemas.responses import FeedbackResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest) -> FeedbackResponse:
    logger.info(
        "Feedback received: analysis_id=%s correct_label=%s",
        request.analysis_id,
        request.correct_label,
    )
    # In production: persist to DB and use for calibration
    return FeedbackResponse(accepted=True, message="Feedback recorded. Thank you.")