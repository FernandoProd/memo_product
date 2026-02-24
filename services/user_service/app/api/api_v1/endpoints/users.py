import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.business_logic.user import UserService
from services.user_service.app.core.security.auth_utils import validate_password
from services.user_service.app.dependencies.user_dependencies import get_current_user, verify_internal_api_key
from services.user_service.app.models import db_helper
from services.user_service.app.schemas.user import (
    UserCreate,
    UserRead,
    UserSchemaForAuth
)
from services.user_service.app.schemas.auth import UserCredentials


logger = logging.getLogger(__name__)

router = APIRouter(tags=["Users"])

@router.post("/", response_model=UserRead)
async def create_user(
        user_data: UserCreate,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    """
    Create a new user.

    - Hashes the password and stores user in database.
    - Returns created user data (without password).
    """
    try:
        logger.info("Creating new user with email: %s", user_data.email)
        service = UserService()
        user = await service.create_user_with_hash(
            session=session,
            user_data=user_data,
        )
        logger.debug("DEBUG: returning user with data: %s",user)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User with this email already exists")

    return user


@router.post("/verify")
async def verify_user_pwd(
        credentials: UserCredentials,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> UserSchemaForAuth:
    """
    Verify user credentials.

    Used internally by auth service to validate login and return user data for JWT payload.
    Returns user info (sub, email, username, roles) if credentials are valid.
    """

    user_service = UserService()
    user = await user_service.get_user_by_email(
        session=session,
        email=credentials.email
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not validate_password(
            password=credentials.password,
            hashed_password=user.hashed_password
    ):
        raise HTTPException(status_code=401 , detail="Invalid password")

    user_for_auth = UserSchemaForAuth(
        sub=str(user.id),
        email=user.email,
        username=user.username,
        roles=[]
    )

    return user_for_auth


@router.get("/me")
async def get_user(
        auth_data: Annotated[dict, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> UserRead:
    """
    Get information about the currently authenticated user.
    """

    user_id = auth_data.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication data",
        )

    logger.debug("Fetching user by ID: %s", user_id)

    service = UserService()
    user = await service.get_user_by_id(session=session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
        user_id: str,
        session: AsyncSession = Depends(db_helper.session_getter),
        _: str = Depends(verify_internal_api_key)
):
    """
    Get user by ID (internal endpoint, protected by API key).
    """
    service = UserService()
    user = await service.get_user_by_id(session=session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user



