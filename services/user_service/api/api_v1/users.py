from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.core.busines_logic.user import UserService
from services.user_service.core.models import db_helper
from services.user_service.core.schemas.user import UserCreate, UserRead
from crud import users as users_crud
from services.user_service.core.security.auth_utils import validate_password
from fastapi import HTTPException

router = APIRouter(tags=["Users"])

@router.post("/", response_model=UserRead)
async def create_user(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        user_data: UserCreate,
):
    service = UserService()
    user = await service.create_user_with_hash(
        session=session,
        user_data=user_data,
    )
    return user


from pydantic import BaseModel, EmailStr

class UserSchemaForAuth(BaseModel):
    sub: str
    email: EmailStr
    username: str
    roles: dict = {} # Можно хранить dict = {"role_auth_user": True, "role_vip_user": False, "role_admin": False} - возможно стоит делать схему этого словаря



# Эта шляпа нужна для того, чтобы дать auth_service payload для jwt, если пароль сходится (можно еще где-нибудь применять)
@router.post("/verify")
async def verify_user_pwd(
        email: str,
        password: str,
        session: AsyncSession = Depends(db_helper.session_getter),
) -> UserSchemaForAuth:
    service = UserService()
    check_user = await service.get_user_by_email(session=session, email=email)


    if not validate_password(
            password=password,
            hashed_password=check_user.hashed_password
    ):
        raise HTTPException(status_code=401 , detail="password is not valid")

    user_for_auth = UserSchemaForAuth(
        sub=str(check_user.id),
        email=check_user.email,
        username=check_user.username,
        roles=[]       # check_user.roles,  # Пока что нигде не добавлены((
    )

    return user_for_auth


# Ручка для получения всей инфы для create access по user_id
@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
        user_id: str,
        session: AsyncSession = Depends(db_helper.session_getter),
):
    service = UserService()
    user = await service.get_user_by_id(session=session, user_id=user_id)
    return user
