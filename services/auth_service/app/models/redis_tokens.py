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
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    revoked: bool = False

    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )

async def save_refresh_token(
    redis_client: redis.Redis,
    refresh_token: str,
    user_id: str,
    ttl_days: int
) -> None:
    try:
        token_data = RedisRefreshToken(user_id=user_id, revoked=False)
        key = f"rt:{refresh_token}"

        # save with ttl (setex getting used for delete our token if it is expired)
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

async def is_token_active(
        redis_client: redis.Redis,
        refresh_token: str,
) -> bool:
    try:
        # We'll check here is token active or not
        key = f"rt:{refresh_token}"
        # If key isn't None we are getting data
        data = await redis_client.get(key)
        if not data:
            return False
        token_data = RedisRefreshToken.model_validate_json(data)
        return not token_data.revoked
    except Exception as e:
        logger.error(f"Error while check if token is active: {e}")
        return False

async def revoke_token(
    redis_client: redis.Redis,
    refresh_token: str
) -> None:
    try:
        # Revoke token
        key = f"rt:{refresh_token}"
        await redis_client.delete(key)
        logger.debug(f"Token revoked from Redis: {refresh_token}")
    except Exception as e:
        logger.error(f"Error while revoke token: {e}")



