import logging

from fastapi import Request

from memo_libs.clients.http_client.user_client import UserServiceClient
from services.auth_service.app.core.config import settings

logger = logging.getLogger(__name__)


def get_user_client() -> UserServiceClient:
    """Dependency for getting UserServiceClient instance."""
    logger.debug(f"Creating UserServiceClient with api_key: {settings.internal_api_key}")
    return UserServiceClient(
        base_url=settings.user_service_url,
        api_key=settings.internal_api_key,
    )


def get_redis_client(request: Request):
    """Dependency for getting Redis client from app state."""
    return request.app.state.redis_client


# print(get_user_client().base_url)