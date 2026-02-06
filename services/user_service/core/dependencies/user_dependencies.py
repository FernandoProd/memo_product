from fastapi import HTTPException, Header, Depends
from services.libs.http_client.auth_client import AuthServiceClient
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def get_auth_client() -> AuthServiceClient:
        return AuthServiceClient()


async def get_current_user(
            authorization: Optional[str] = Header(None),
            http_client: AuthServiceClient = Depends(get_auth_client)
) -> dict:
    logger.debug("get_current_user called with authorization: %s", authorization)
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid Authorization header"
        )

    token = authorization.split("Bearer ")[1]
    logger.debug("Extracted token: %s", token)

    try:
        response = await http_client.get_current_user(token)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Invalid token"
            )

        auth_data = response.json()
        logger.info("get_current_user returning: %s", auth_data)
        return auth_data  # {"user_id": "...", "email": "...", ...}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))