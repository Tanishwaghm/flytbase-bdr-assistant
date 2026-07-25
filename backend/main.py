"""
FlytBase Inbound BDR Assistant - Backend Entrypoint

Run locally:
    uvicorn main:app --reload --port 8000

Deployed on Render (see /docs/README.md for deployment instructions).
"""
import logging
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.api.routes import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("main")

settings = get_settings()

app = FastAPI(
    title="FlytBase Inbound BDR Assistant API",
    description="AI-agent pipeline that automates inbound lead qualification, research, and outreach.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start) * 1000
    logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({duration_ms:.0f}ms)")
    return response


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception on {request.url.path}")
    return JSONResponse(status_code=500, content={"detail": "Internal server error."})


app.include_router(router, prefix="/api")


@app.get("/")
def root():
    return {
        "service": "FlytBase Inbound BDR Assistant API",
        "status": "running",
        "docs": "/docs",
    }
