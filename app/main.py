"""Main FastAPI application module."""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.v1 import combined, timezone, weather
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.services.cache import cache_service

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting up Timezone Weather API...")
    await cache_service.connect()
    yield
    logger.info("Shutting down Timezone Weather API...")
    await cache_service.disconnect()


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="API for timezone information and weather data with witty messages",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Prometheus metrics
Instrumentator().instrument(app).expose(app)

# Include routers
app.include_router(timezone.router, prefix="/api/v1", tags=["Timezone"])
app.include_router(weather.router, prefix="/api/v1", tags=["Weather"])
app.include_router(combined.router, prefix="/api/v1", tags=["Combined"])


@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "timezone": "/api/v1/timezone/{timezone}",
            "current_weather": "/api/v1/weather/current",
            "forecast": "/api/v1/weather/forecast",
            "combined": "/api/v1/timezone-weather",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    redis_status = "healthy" if await cache_service.ping() else "unhealthy"
    return {
        "status": "healthy",
        "redis": redis_status,
        "version": settings.APP_VERSION,
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )