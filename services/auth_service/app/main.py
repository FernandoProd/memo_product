import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from memo_libs.logging.log_config import setup_logging
from services.auth_service.app.api.api_v1.endpoints.auth import router as auth_router
from services.auth_service.app.core.config import settings
from services.auth_service.app.models.redis_pool import get_redis_pool

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application lifecycle.
    Creates Redis connection pool on startup and closes it on shutdown.
    """

    # Create Redis connection pool
    redis_client = await get_redis_pool()
    app.state.redis_client = redis_client
    logger.info("Redis connection pool created")

    yield

    # Close connections
    await redis_client.close()
    logger.info("Redis connection pool closed")


def create_app() -> FastAPI:
    """FastAPI application factory"""

    app = FastAPI(
        title="Auth Service",
        description="Authentication service with JWT token management",
        lifespan=lifespan,
        version="1.0.0",
        swagger_ui_parameters={
            "persistAuthorization": True,
            "withCredentials": True,
        }
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.auth_service_url, settings.auth_service_url],  # frontend/Swagger
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth_router)

    return app

# Create application instance
app = create_app()


if __name__ == "__main__":
    # Development server runner
    logger.debug("some information for debug")
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info",
    )