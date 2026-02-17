from fastapi import FastAPI
from services.auth_service.app.api.api_v1.endpoints.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from memo_libs.logging.log_config import setup_logging
from services.auth_service.app.models.redis import get_redis_pool
from contextlib import asynccontextmanager
import logging


setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём пул соединений
    redis_client = await get_redis_pool()
    app.state.redis_client = redis_client
    yield
    # Закрываем соединения
    await redis_client.close()
app = FastAPI(
    title="Auth Service",
    lifespan=lifespan,
    swagger_ui_parameters={
        "persistAuthorization": True,
        "withCredentials": True,
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001", "http://0.0.0.0:8001"],  # адрес твоего frontend/Swagger
    allow_credentials=True,  # ← САМОЕ ВАЖНОЕ!
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

if __name__ == "__main__":
    logger.debug("some information for debug")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)