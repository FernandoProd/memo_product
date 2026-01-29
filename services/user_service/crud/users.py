from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from services.user_service.core.models import User
from sqlalchemy import select

from services.user_service.core.schemas.user import UserCreate, UserCreateInternal
from typing import Optional #ОПять забыл нахрена тут Optional

async def get_all_users(
        session: AsyncSession
) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()

async def create_user(
        session: AsyncSession,
        user_create: UserCreateInternal,
) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    # await session.refresh(user)
    return user


async def get_user_by_id(
        session: AsyncSession,
        user_id: str,
) -> Optional[User]:
    try:
        # Преобразуем строку в UUID объект
        from sqlalchemy.dialects.postgresql import UUID
        import uuid

        #user_uuid = uuid.UUID(user_id)

        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    except (ValueError, Exception) as e:
        print(f"Ошибка: {e}")
        return None