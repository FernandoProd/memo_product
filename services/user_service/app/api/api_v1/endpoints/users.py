import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from services.user_service.app.busines_logic.user import UserService
from services.user_service.app.core.security.auth_utils import validate_password
from services.user_service.app.dependencies.user_dependencies import get_current_user, verify_internal_api_key
from services.user_service.app.models import db_helper
from services.user_service.app.schemas.user import UserCreate, UserRead


logger = logging.getLogger(__name__)
router = APIRouter(tags=["Users"])

@router.post("/", response_model=UserRead)
async def create_user(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        user_data: UserCreate,
):
    logger.info("Вызов эндпоинта для создания пользователя")
    service = UserService()
    user = await service.create_user_with_hash(
        session=session,
        user_data=user_data,
    )
    logger.debug("DEBUG: возвращаем значение user - %s",user)
    return user


from pydantic import BaseModel, EmailStr

class UserSchemaForAuth(BaseModel):
    sub: str
    email: EmailStr
    username: str
    roles: list= [] # Можно хранить dict = {"role_auth_user": True, "role_vip_user": False, "role_admin": False} - возможно стоит делать схему этого словаря



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


@router.get("/me")
async def get_user(
        session: AsyncSession = Depends(db_helper.session_getter),
        auth_data: dict = Depends(get_current_user),
) -> UserRead:
    logger.debug("Сообщение для отладки")
    logger.debug("Сообщение для отладки")
    logger.debug("Сообщение для отладки")
    logger.debug("Сообщение для отладки")
    # Изначально был user_id
    user_id = auth_data.get("user_id")
    print(f"DEBUG: user_id = {user_id}")
    logger.debug(f"Troubles with something shit: {user_id}")
    service = UserService()
    user_data = await service.get_user_by_id(session=session, user_id=user_id)
    return user_data



# Ручка для получения всей инфы для create access по user_id
# Учесть, что тут не защищена ручка, то есть каждый сможет получить без авторизации информацию
@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
        user_id: str,
        session: AsyncSession = Depends(db_helper.session_getter),
        _: str = Depends(verify_internal_api_key)
):
    service = UserService()
    user = await service.get_user_by_id(session=session, user_id=user_id)
    return user


# @router.get("/me")
# async def get_user(
#         session: AsyncSession = Depends(db_helper.session_getter),
#         auth_data: dict = Depends(get_current_user),
# ) -> UserRead:
#     logger.debug("Сообщение для отладки")
#     logger.debug("Сообщение для отладки")
#     logger.debug("Сообщение для отладки")
#     logger.debug("Сообщение для отладки")
#     # Изначально был user_id
#     user_id = auth_data.get("id")
#     print(f"DEBUG: user_id = {user_id}")
#     logger.debug(f"Troubles with something shit: {user_id}")
#     service = UserService()
#     user_data = await service.get_user_by_id(session=session, user_id=user_id)
#     return user_data

