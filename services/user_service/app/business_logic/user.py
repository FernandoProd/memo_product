import logging
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.core.security.auth_utils import hash_password
from services.user_service.app.crud import users as crud_users
from services.user_service.app.schemas.user import (
    UserCreate,
    UserCreateInternal,
    UserRead,
)
from services.user_service.app.models import User


logger = logging.getLogger(__name__)


class UserService:
    async def create_user_with_hash(
            self,
            session: AsyncSession,
            user_data: UserCreate,
    ) -> UserRead:
        """Create a new user with hashed password"""

        # Checking email that it's already exists
        existing = await crud_users.get_user_by_email(session, user_data.email)
        if existing:
            logger.warning("Attempt to create user with existing email: %s", user_data.email)

            raise IntegrityError("User with this email already exists")

        hashed_pwd = hash_password(user_data.password)
        user_dict = UserCreateInternal(
            username = user_data.username,
            email = user_data.email,
            hashed_password = hashed_pwd,
        )

        try:
            user = await crud_users.create_user(
                session=session,
                user_create = user_dict,
            )
        except IntegrityError:
            logger.exception("Failed to create user due to integrity error")
            raise

        return UserRead.model_validate(user)


    async def get_user_by_id(
            self,
            session: AsyncSession,
            user_id: str
    ) -> UserRead | None:
        """
        Get user by ID
        Returns None if not found
        """

        user = await crud_users.get_user_by_id(
            session=session,
            user_id=user_id,
        )
        if user is None:
            logger.debug("User with ID: %s - not found", user_id)

        return user


    async def get_user_by_email(
            self,
            session: AsyncSession,
            email: str
    ) -> User | None:
        """
        Get user by email
        Returns None if not found
        """

        user = await crud_users.get_user_by_email(
            session=session,
            email=email,
        )

        if user is None:
            logger.debug("User with email: %s - not found", email)

        return user
















