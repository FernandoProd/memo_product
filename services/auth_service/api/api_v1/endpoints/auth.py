from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response, Request
from core.schemas.schemas import TokenResponse, LoginRequest, RefreshTokenRequest, LogoutRequest
from fastapi.security import HTTPBearer
from fastapi import HTTPException, status
from services.auth_service.auth.dependencies import get_current_token_payload, oauth2_scheme
from services.auth_service.auth.helpers import create_access_token, create_refresh_token
from services.auth_service.utils.jwt_utils import decode_jwt
from services.auth_service.core.busines_logic.auth_server import AuthService
from typing import Annotated
from services.auth_service.core.models.db_helper import db_helper
import logging

logger = logging.getLogger(__name__)
# Написать http_client для подключения
# Зависимость для получения HTTP-клиента


http_bearer = HTTPBearer(auto_error=False)


router = APIRouter(prefix="/auth", tags=["Authentication"], dependencies=[Depends(http_bearer)])

# api/v1/endpoints/auth.py
from pydantic import BaseModel

class UserData(BaseModel):
    username: str
    password: str
    email: str

from services.libs.http_client.user_client import UserServiceClient
from services.libs.clients.exceptions import *


def get_user_client() -> UserServiceClient:
    return UserServiceClient()

# Логин - получение токенов по login_data
@router.post("/login", response_model=TokenResponse)
async def login(
        fastapi_response: Response,
        login_data: LoginRequest,
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        http_client: UserServiceClient = Depends(get_user_client),
):
    # user = get_user_by_email(session, login_data.email)
    # Если пользователя нет, то ошибка
    # Сравниваем хешированный пароль login_data.password и user.hashed_password
    # Создаем токены access и refresh
    # Сохранить refresh_token в таблицу
    # Вернуть TokenResponse
    try:
        user_service_response = await http_client.verify_password(login_data.email, login_data.password)
        user_data = user_service_response.json()
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except UserServiceUnavailableError:
        raise HTTPException(status_code=503, detail="User service unavailable")
    except UserServiceError:
        raise HTTPException(status_code=500, detail="Internal server error")

    #user_data = user_service_response.json()
    # Получаем Sub, username, email

    # Создаем токены
    access_token = create_access_token(
        user=user_data
    )
    refresh_token = create_refresh_token(
        user=user_data
    )

    # add refresh token into db
    service = AuthService()
    await service.add_token_info_into_db(
        session=session,
        refresh_token=refresh_token,
    )
    # Надо ли хешировать refresh и access перед отправкой в БД и в куки?
    # Сохраняем refresh_token в базу (если нужно)
    # ... код сохранения refresh_token ...

    # Помещаем refresh в кукисы

    fastapi_response.set_cookie(
        key="refresh_token",  # name of cookie
        value=refresh_token,  # value
        httponly=True,
        secure=True,          # only https
        samesite="strict",    # security of CSRF Есть еще и другие штуки
        max_age=60 * 60 * 24 * 30  # срок жизни 30 дней
        # domain=".myapp.com" в продакшине указать для каких доменов
    )

    return TokenResponse(
        access_token=access_token,
        # refresh_token=refresh_token,
        token_type="bearer"
    )


# Обновление access токена
@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
        fastapi_request: Request,
        # fastapi_response: Response,
        http_client: UserServiceClient = Depends(get_user_client),
):
    refresh_token = fastapi_request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(401, "No refresh token")

    # 1. Проверка что тип токена "refresh"
    # 1. Сравнение токена с БД
    # 2. Обновление refresh token и загрузка его в куки
    # Сравнение token_data.type != "refresh" - ошиббка  ВАЖНО СРАВНИТЬ С БД
    # все ок - создаем токен новый

    payload = decode_jwt(refresh_token) # Стоит проверять срок действия
    user_id = payload["sub"]

    try:
        user_service_response = await http_client.get_user_by_id(user_id)
        user_data = user_service_response.json()
    except HTTPException as e:
        print(f" На этом этапе залупа какая-то")
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    user = {
        "sub": user_data["id"],
        "email": user_data["email"],
        "username": user_data["username"],
        "roles": [],
    }
    new_access_token = create_access_token(user)
    # new_refresh_token = create_refresh_token() # Опционально , но тогда надо будет записать новый refresh в куки

    return TokenResponse(
        access_token=new_access_token,
        token_type="bearer"
    )


@router.post("/verify_token")
async def verify_token(token_data: dict):
    logger.debug("Info about token data: %s", token_data)
    token = token_data.get("token")
    logger.debug("Token: %s", token)
    payload = decode_jwt(token)

    logger.debug("user_id: %s", payload.get("sub"))
    logger.debug("email: %s", payload.get("email"))

    # Возврат пользователя можно реализовать в виде pydantic model
    return {
        "valid": True,
        "user_id": payload.get("sub"),
        "email": payload.get("email"),
    }



# По сюда комментировал

#
#
# Получение данных авторизованного пользователя
# @router.get("/users/me/", dependencies=[Depends(oauth2_scheme)])
# def auth_user_check_self_info(
#         payload: dict = Depends(get_current_token_payload),
#        # user: UserSchema = Depends(get_current_active_auth_user), # Этот метод для того, чтобы можно было проверять пользователя по token и public_key
# ):
#     iat = payload.get("iat") # когда выпущен
#     jti = payload.get("jti") # идентификационный номер токена
#
#     # return {
#     #     "username": user.username,
#     #     "email": user.email,
#     #     "logged_in_at": iat,
#     #     "jti": jti,
#     # }
#     pass
    # token = credentials.credentials
    # payload = Проверка токена (token)
    # Если payload.type != "access" - ошибка
    # Если payload.sub нет, то не найден пользователь
    # Вернуть UserInfo или UserData
    # нужен эндпоинт для получения текущей сессии (то есть получения данных текущего пользователя)
#
#
# # Выход (отзыв токена)
# @router.post("/logout")
# async def logout(
#         session: AsyncSession,
#         logout_request: LogoutRequest,
# ):
#     # Если использую БД для refresh токенов
#     # await revoke_refresh_token(session, logout_request.refresh_token)
#
#     # Для stateless JWT - клиент просто удаляет токены
#     # Инвалидируем сессию
#     pass
#

#
# # @router
# async def change_password(
#         old_password: str,
#         new_password: str,
#         credentials: OAuth2PasswordRequestForm = Depends(),
#         session: AsyncSession = Depends(),
# ):
#     pass
#
# # @router
# def update_user():
#     pass
#     # обновления логина и пароля
#
# # dependency
# # async get current user
#
#
# #Для проверки ролей, но можно придумать и другие роли
# # async get_current)admin_user
#
#
#
# # 7. Использование в других сервисах:
# # python
# # # В user_service или других сервисах
# # from fastapi import Depends
# # from auth_service.core.dependencies import get_current_user
# #
# # @router.get("/protected")
# # async def protected_route(
# #     current_user: User = Depends(get_current_user)
# # ):
# #     return {"message": f"Hello {current_user.username}"}