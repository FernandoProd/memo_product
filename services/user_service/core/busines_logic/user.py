import crud.users
from core.models import User
from core.schemas.user import UserCreateInternal
from crud.users import UserCreate
from core.security.auth_utils import hash_password
from sqlalchemy.ext.asyncio import AsyncSession

class UserService:
    async def create_user_with_hash(self, session: AsyncSession, user_data: UserCreate) -> User:
        hashed_pwd = hash_password(user_data.password)
        user_dict = UserCreateInternal(
            username = user_data.username,
            email = user_data.email,
            hashed_password = hashed_pwd,
        )
        user = await crud.users.create_user(
            session=session,
            user_create = user_dict,
        )
        return user


    async def get_user_by_id(self, session: AsyncSession, user_id: str) -> User:
        user = await crud.users.get_user_by_id(
            session=session,
            user_id=user_id,
        )

        if not user:
            raise "User not found"

        return user
