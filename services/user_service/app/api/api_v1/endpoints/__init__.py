from fastapi import APIRouter

from services.user_service.app.api.api_v1.endpoints.users import router as users_router
from services.user_service.app.core.config import settings

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(
    users_router,
    prefix=settings.api.v1.users
)
