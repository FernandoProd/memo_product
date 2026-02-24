from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.core.security.auth_utils import hash_password
from services.user_service.app.crud import users
from services.user_service.app.schemas.user import (
    UserCreate,
    UserCreateInternal,
    UserRead
)

class UserService:
    async def create_user_with_hash(self, session: AsyncSession, user_data: UserCreate) -> UserRead:
        hashed_pwd = hash_password(user_data.password)
        user_dict = UserCreateInternal(
            username = user_data.username,
            email = user_data.email,
            hashed_password = hashed_pwd,
        )
        user = await users.create_user(
            session=session,
            user_create = user_dict,
        )
        return user


    async def get_user_by_id(self, session: AsyncSession, user_id: str) -> UserRead:
        user = await users.get_user_by_id(
            session=session,
            user_id=user_id,
        )

        if not user:
            raise HTTPException(status_code=404, detail=f"User not found {user}")

        return user


    async def get_user_by_email(
            self,
            session: AsyncSession,
            email: str
    ) -> UserRead:
        user = await users.get_user_by_email(
            session=session,
            email=email,
        )

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user
















