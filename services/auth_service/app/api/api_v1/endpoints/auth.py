import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import HTTPBearer
from httpx import HTTPStatusError
from sqlalchemy.ext.asyncio import AsyncSession

from memo_libs.clients.exceptions import (
    InvalidCredentialsError,
    UserServiceError,
    UserServiceUnavailableError,
)
from memo_libs.clients.http_client.user_client import UserServiceClient

from services.auth_service.app.auth.helpers import create_access_token, create_refresh_token
from services.auth_service.app.business_logic.auth_server import AuthService
from services.auth_service.app.core.config import settings
from services.auth_service.app.models.db import db_helper
from services.auth_service.app.models.redis_tokens import is_token_active, save_refresh_token
from services.auth_service.app.schemas.schemas import LoginRequest, TokenResponse
from services.auth_service.app.utils.jwt_utils import decode_jwt
from services.auth_service.app.api.dependencies import get_redis_client, get_user_client


logger = logging.getLogger(__name__)

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix="/auth", tags=["Authentication"], dependencies=[Depends(http_bearer)])


@router.post("/login", response_model=TokenResponse)
async def login(
        request: Request,
        fastapi_response: Response,
        login_data: LoginRequest,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        http_client: Annotated[UserServiceClient, Depends(get_user_client)],
) -> TokenResponse:
    """
    Authenticate user and return access/refresh tokens.

    - Validates credentials with user service
    - Creates JWT tokens
    - Stores refresh token in Redis and database
    - Sets refresh token as HTTP-only cookie
    """

    try:
        # Verify credentials with user service
        user_service_response = await http_client.verify_password(
            login_data.email,
            login_data.password
        )
        user_data = user_service_response.json()
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except UserServiceUnavailableError:
        raise HTTPException(status_code=503, detail="User service unavailable")
    except UserServiceError:
        logger.exception("Unexpected error from user service")
        raise HTTPException(status_code=500, detail="Internal server error")

    # Fetching user information
    user_id = user_data["sub"]
    # user_info = {}

    # Creating tokens
    access_token = create_access_token(user=user_data)
    refresh_token = create_refresh_token(user=user_data)


    # Store refresh token in Redis
    redis_client = get_redis_client(request)
    await save_refresh_token(
        redis_client=redis_client,
        refresh_token=refresh_token,
        user_id=user_id,
        ttl_days=settings.auth_jwt.refresh_token_expire_days
    )

    # Store refresh token in database
    service = AuthService()
    await service.add_token_info_into_db(
        session=session,
        refresh_token=refresh_token,
    )

    # Set refresh token as HTTP-only cookie
    fastapi_response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,                # only https
        samesite="strict",          # security of CSRF and there are a different other things
        max_age=60 * 60 * 24 * 30
        # domain=".memoproduct.com"       # set in the future
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
        request: Request,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        http_client: Annotated[UserServiceClient, Depends(get_user_client)],
        redis_client: Annotated[Any, Depends(get_redis_client)],
) -> TokenResponse:
    """
    Refresh access token using refresh token from cookie.
    """

    # Get refresh token from cookie
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(401, "No refresh token")

    # Check: is refresh token active?
    token_valid = await is_token_active(
        redis_client=redis_client,
        refresh_token=refresh_token,
    )

    if not token_valid:
        # Check database if not in Redis
        auth_service = AuthService()
        token_valid = await auth_service.refresh_token_into_db(
            session=session,
            refresh_token=refresh_token,
        )

    if not token_valid:
        raise HTTPException(status_code=401, detail="Invalid or revoked refresh token")

    # Decode and validate token
    try:
        payload = decode_jwt(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload["sub"]
    except Exception as e:
        logger.warning(f"Failed to decode refresh token: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

    # Get fresh user data
    try:
        user_service_response = await http_client.get_user_by_id(user_id)
        user_data = user_service_response.json()
    except HTTPStatusError as e:
        logger.error(f"User service error: {e}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail="User service error",
        )

    # Create new access token (and refresh in the future)
    user = {
        "sub": user_data["id"],
        "email": user_data["email"],
        "username": user_data["username"],
        "roles": [],
    }

    new_access_token = create_access_token(user)
    # new_refresh_token = create_refresh_token()    # In the future

    return TokenResponse(
        access_token=new_access_token,
        token_type="bearer"
    )


@router.post("/verify_token")
async def verify_token(
        token_data: dict
) -> dict:
    """
    Verify JWT token and return user information.
    Used internally by other services.
    """

    token = token_data.get("token")
    if not token:
        raise HTTPException(status_code=400, detail="Token is required")

    try:
        payload = decode_jwt(token)
    except Exception as e:
        logger.warning(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")

    # Implement user's refund as pydantic model in the future
    return {
        "valid": True,
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
    }


@router.post("/logout", status_code=200)
async def logout(
        request: Request,
        response: Response,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        redis_client: Annotated[Any, Depends(get_redis_client)],
):
    """
    Logout user by revoking refresh token.
    """

    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="No refresh token in cookies")

    # Remove from Redis
    await redis_client.delete(f"rt:{refresh_token}")

    # Remove from database
    auth_service = AuthService()
    revoked_token = await auth_service.revoke_refresh_token(
        session=session,
        refresh_token=refresh_token,
    )

    if not revoked_token:
        logger.warning(f"Attempt to revoke non-existent token: {refresh_token}")

    # Clear cookie
    response.delete_cookie(
        key="refresh_token",
        path="/",
        secure=True,
        httponly=True,
        samesite="strict"
    )

    return {"message": "Logged out successfully"}


