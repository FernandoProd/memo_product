import redis.asyncio as redis
from services.auth_service.app.core.config import settings

async def get_redis_pool():
    return redis.from_url(
        str(settings.redis.url),
        socket_timeout=settings.redis.socket_timeout,
        socket_connect_timeout=settings.redis.socket_connect_timeout,
        decode_responses=True,
    )