import logging

from fastapi import HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from memo_libs.clients import AuthServiceClient
from services.user_service.app.core.config import settings

logger = logging.getLogger(__name__)

bearer_scheme = HTTPBearer(auto_error=False)

def get_auth_client() -> AuthServiceClient:
    logger.debug("Вызвался get_auth_client")
    return AuthServiceClient(base_url="http://localhost:8001")


async def get_current_user(
            credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
            http_client: AuthServiceClient = Depends(get_auth_client)
) -> dict:
    logger.debug("get_current_user called with credentials: %s", credentials)

    # 1. Проверяем, есть ли заголовок
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. Извлекаем токен (HTTPBearer уже проверил формат "Bearer <token>")
    token = credentials.credentials
    logger.debug("Достали токен из хедера: %s", token)
    try:
        response = await http_client.get_current_user(token)
        logger.debug("Вот ответ от /auth/verify_token: %s", response)
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




async def verify_internal_api_key(x_internal_api_key: str = Header(...)) -> str:
    if x_internal_api_key != settings.internal_api_key:
        raise HTTPException(status_code=401, detail="Invalid internal API key")
    return x_internal_api_key