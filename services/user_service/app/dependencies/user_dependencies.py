import logging
from typing import Dict, Any

import httpx
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from memo_libs.clients import AuthServiceClient
from services.user_service.app.core.config import settings

logger = logging.getLogger(__name__)

bearer_scheme = HTTPBearer(auto_error=False)

def get_auth_client() -> AuthServiceClient:
    """Dependency to get an instance of AuthServiceClient"""
    logger.debug("Creating AuthServiceClient")
    return AuthServiceClient(base_url=settings.auth_service_url)


async def get_current_user(
            credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
            http_client: AuthServiceClient = Depends(get_auth_client)
) -> Dict[str, Any]:
    """
    Validate JWT token and return user data from auth service
    """

    logger.debug("get_current_user called with credentials: %s", credentials)

    # Check if Authorization header is present
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    logger.debug("Validating token with auth service")
    try:
        response = await http_client.get_current_user(token)
    except httpx.RequestError as e:
        logger.error(f"Auth service connection error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service temporarily unavailable",
        )
    except Exception as e:
        logger.exception("Unexpected error during token validation")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    # Handle non-200 responses from auth service
    if response.status_code != status.HTTP_200_OK:
        logger.warning(f"Auth service returned {response.status_code} for token validation")
        raise HTTPException(
            status_code=response.status_code,
            detail="Invalid or expired token",
        )

    # Parse and validate response body
    try:
        auth_data = response.json()
    except ValueError:
        logger.error("Auth service returned invalid JSON")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid response from authentication service",
        )

    # Checking that required fields are present
    if "user_id" not in auth_data:
        logger.error("Auth service response missing 'user_id' field")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid response from authentication service",
        )

    logger.debug("Token validated successfully for user_id: %s", auth_data["user_id"])
    return auth_data


async def verify_internal_api_key(x_internal_api_key: str = Header(...)) -> str:
    """
    Verify internal API key for service-to-service communication
    """
    if x_internal_api_key != settings.internal_api_key:
        logger.warning("Invalid internal API key attempt")
        raise HTTPException(
            status_code=401,
            detail="Invalid internal API key"
        )

    return x_internal_api_key