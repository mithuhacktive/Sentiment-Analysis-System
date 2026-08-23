from __future__ import annotations
import logging
import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.config import get_settings
from app.database import init_db
from app.ml.model import get_model
from app.api import health, analyze, feedback

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("SentiGuard starting — env=%s offline=%s", settings.sentiguard_env, settings.sentiguard_offline)
    await init_db()
    model = get_model()
    try:
        model.load()
        logger.info("Model ready")
    except Exception as e:
        logger.error("Model failed to load: %s — continuing in degraded mode", e)
    yield
    logger.info("SentiGuard shutting down")


app = FastAPI(
    title="SentiGuard",
    description="Real-time evidence-grounded product sentiment intelligence",
    version="1.0.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    start = time.perf_counter()
    response = await call_next(request)
    ms = round((time.perf_counter() - start) * 1000, 1)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-Ms"] = str(ms)
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(status_code=500, content={"error": "internal_server_error", "detail": str(exc)})


PREFIX = "/api/v1"
app.include_router(health.router, prefix=PREFIX, tags=["health"])
app.include_router(analyze.router, prefix=PREFIX, tags=["analyze"])
app.include_router(feedback.router, prefix=PREFIX, tags=["feedback"])
