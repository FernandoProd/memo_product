from app.api.api_v1.endpoints.users import router as api_router
from fastapi import FastAPI
from services.user_service.app.core.config import settings

main_app = FastAPI()
main_app.include_router(api_router, prefix=settings.api.prefix)

# print(settings.api.prefix) # /api
# print(settings.api.v1.prefix) # /v1
