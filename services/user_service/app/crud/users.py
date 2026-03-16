import logging
from typing import Optional, Sequence

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.models import User
from services.user_service.app.schemas.user import UserCreateInternal


logger = logging.getLogger(__name__)


async def get_all_users(
        session: AsyncSession
) -> Sequence[User]:
    """Get all users ordered by ID"""
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()

async def create_user(
        session: AsyncSession,
        user_create: UserCreateInternal,
) -> User:
    """
    Create a new user in the database.
    """

    user = User(**user_create.model_dump())
    session.add(user)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        logger.error("Integrity error creating user with email %s: %s", user_create.email, e)
        raise

    return user


async def get_user_by_id(
        session: AsyncSession,
        user_id: str,
) -> Optional[User]:
    """
    Get user by UUID string
    Returns None if not found or invalid UUID
    """

    try:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    except Exception as e:
        logger.exception("Unexpected error while fetching user by ID %s", user_id)

        return None


async def get_user_by_email(
        session: AsyncSession,
        email: str,
) -> Optional[User]:
    """
    Get user by email
    Returns None if not found
    """

    try:
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    except Exception as e:
        logger.exception("Unexpected error while fetching user by email %s", email)

        return None


async def update_user_data(
        session: AsyncSession,
        user_id: str, # will be put in by auto with maybe Dependency
        first_name: str,
        last_name: str,
) -> User | None:
    """
    Update first name and last name for user
    return None if not found
    """

    user = await session.get(User, user_id)
    if not user:
        return None

    user.first_name = first_name
    user.last_name = last_name

    try:
        await session.commit()
        await session.refresh(user)  # actual info from db
        return user
    except IntegrityError as e:
        await session.rollback()
        logger.error("Integrity error updating user %s: %s", user_id, e)
        raise
    except Exception as e:
        await session.rollback()
        logger.error("Unexpected error updating user %s: %s", user_id, e)
        raise