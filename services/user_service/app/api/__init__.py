from fastapi import APIRouter
from services.user_service.app.api.api_v1 import router as router_api_v1
from services.user_service.app.core.config import settings


router = APIRouter(prefix=settings.api.prefix)
router.include_router(
    router_api_v1
)