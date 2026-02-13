from fastapi import APIRouter
from core.config import settings
from .users import router as users_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(
    users_router,
    prefix=settings.api.v1.users
)


print(router.prefix)
# services.user_service.app.api.api_v1.endpoints