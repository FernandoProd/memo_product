from app.api.api_v1.endpoints.users import router as api_router
from fastapi import FastAPI
from .core.config import settings

main_app = FastAPI()
main_app.include_router(api_router, prefix=settings.api.prefix)
print(api_router.prefix)
print(settings.api)