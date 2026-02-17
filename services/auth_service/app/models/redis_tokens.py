import redis.asyncio as redis
from typing import Optional
import json
import logging
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, ConfigDict

from services.auth_service.app.core.config import settings
import asyncio

logger = logging.getLogger(__name__)


class RedisRefreshToken(BaseModel):
    user_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )

async def save_refresh_token(
    redis_client: redis.Redis,
    refresh_token: str,
    user_id: int,
    ttl_days: int
) -> None:
    try:
        token_data = RedisRefreshToken(user_id=user_id)
        key = f"rt:{refresh_token}"

        # save with ttl
        result = await redis_client.setex(
            key,
            ttl_days * 24 * 60 * 60,
            token_data.model_dump_json()
        )
        logger.debug(f"Refresh token saved to Redis for user {user_id}")
        return result

    except Exception as e:
        logger.error(f"Error while saving refresh token for user: {e}")

async def get_user_id_by_refresh_token():
    pass

async def delete_refresh_token():
    pass


async def test_redis_saving():
    redis_client = redis.from_url(settings.redis.url, decode_responses=True) # decode_responses нужен для возвращение строк, а не байтов

    await save_refresh_token(
        redis_client=redis_client,
        refresh_token = "refresh-token-for-test",
        user_id=1,
        ttl_days=7
    )

    result = await redis_client.get(f"rt:refresh-token-for-test")
    await redis_client.aclose() # Может async with лучше использовать?
    return result

# if __name__ == "__main__":
#     asyncio.run(test_redis_saving())

print(asyncio.run(test_redis_saving()))

# Для запуска из корня всего проекта
# PYTHONPATH=. python services/auth_service/app/models/redis_tokens.py


# async def simple_test():
#     redis_client = redis.from_url(str(settings.redis.url), decode_responses=True)
#
#     # Простая запись
#     await redis_client.setex("test:key", 60, "Hello Redis!")
#
#     # Простое чтение
#     value = await redis_client.get("test:key")
#     print(f"Значение: {value}")
#
#     await redis_client.aclose()
#     return value
#
#
# if __name__ == "__main__":
#     result = asyncio.run(simple_test())
#     print(f"Результат: {result}")