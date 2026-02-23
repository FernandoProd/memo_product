import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from memo_libs.logging.log_config import setup_logging

from services.user_service.app.api import router as api_router # Перепроверить
from services.user_service.app.core.config import settings
from services.user_service.app.models.db import db_helper


# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages application lifecycle.
    Closes database connections on shutdown.
    """

    logger.info("Starting up user service...")

    yield

    logger.info("Shutting down user service, disposing database engine...")

    await db_helper.dispose()
    logger.info("Database engine disposed.")


def create_app() -> FastAPI:
    """FastAPI application factory for user service"""

    app = FastAPI(
        title="User Service",
        description="User management service",
        version="1.0.0",
        lifespan=lifespan,
        default_response_class=ORJSONResponse,  # faster JSON serialization
        swagger_ui_parameters={
            "persistAuthorization": True,
        },
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(api_router)

    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    # Development server runner
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info",
    )

# http://127.0.0.1:8000