from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from fastapi.responses import ORJSONResponse

from api import router as api_router
from core.config import settings
from core.models.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup

    yield
    # shutdown
    print("dispose engine")
    await db_helper.dispose()


# ORJSONResponse быстрее отправляет байтики
main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

main_app.include_router(api_router, prefix=settings.api.prefix)


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )

# http://127.0.0.1:8000