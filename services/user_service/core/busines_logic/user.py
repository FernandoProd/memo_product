from services.user_service.crud import users
from services.user_service.core.models import User
from services.user_service.core.schemas.user import UserCreateInternal
from services.user_service.crud.users import UserCreate
from services.user_service.core.security.auth_utils import hash_password
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Header, Depends
from services.libs.http_client.auth_client import AuthServiceClient
from services.libs.clients.exceptions import *
from typing import Optional

class UserService:
    async def create_user_with_hash(self, session: AsyncSession, user_data: UserCreate) -> User:
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


    async def get_user_by_id(self, session: AsyncSession, user_id: str) -> User:
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
    ) -> User:
        user = await users.get_user_by_email(
            session=session,
            email=email,
        )

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user


#     def get_auth_client(self) -> AuthServiceClient:
#         return AuthServiceClient()
#
#
#     async def get_current_user(
#             self,
#             authorization: Optional[str] = Header(None),
#             http_client: AuthServiceClient = Depends(get_auth_client)
# ) -> dict:
#         if not authorization.startswith("Bearer "):
#             raise HTTPException(status_code=401, detail="Invalid authorization header")
#
#         if not authorization or not authorization.startswith("Bearer "):
#             raise HTTPException(
#                 status_code=401,
#                 detail="Missing or invalid Authorization header"
#             )
#
#         token = authorization.split("Bearer ")[1]
#
#         try:
#             response = await http_client.get_current_user(token)
#
#             if response.status_code != 200:
#                 raise HTTPException(
#                     status_code=response.status_code,
#                     detail="Invalid token"
#                 )
#
#             auth_data = response.json()
#             return auth_data  # {"user_id": "...", "email": "...", ...}
#
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=str(e))















