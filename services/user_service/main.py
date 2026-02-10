import logging
import sys


# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('app.log'),
#         logging.StreamHandler(sys.stdout)
#     ]
# )
#
# # Устанавливаем уровень для библиотек
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# logging.getLogger('uvicorn').setLevel(logging.INFO)



from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from fastapi.responses import ORJSONResponse

from api import router as api_router
from core.config import settings
from core.models.db_helper import db_helper
from services.user_service.core.logging.log_config import setup_logging

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