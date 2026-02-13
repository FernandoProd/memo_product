import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from fastapi.responses import ORJSONResponse

from app.api import router as api_router
from app.core.config import settings
from core.models.db_helper import db_helper
from memo_libs.logging.log_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup

    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()


logger.debug("Отладочное сообщение")

# ORJSONResponse быстрее отправляет байтики
main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
logger.debug("Отладочное сообщение")
main_app.include_router(api_router, prefix=settings.api.prefix)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        log_level=None,
        reload=True,
    )

# http://127.0.0.1:8000