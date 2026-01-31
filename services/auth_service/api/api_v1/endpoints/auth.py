from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession


from core.schemas.schemas import TokenResponse, LoginRequest, RefreshTokenRequest, LogoutRequest
from fastapi.security import HTTPBearer
from fastapi import HTTPException, status
from services.auth_service.auth.dependencies import get_current_token_payload, oauth2_scheme
from services.auth_service.auth.helpers import create_access_token, create_refresh_token


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
        login_data: LoginRequest,
        http_client: UserServiceClient = Depends(get_user_client),
):
    # user = get_user_by_email(session, login_data.email)
    # Если пользователя нет, то ошибка
    # Сравниваем хешированный пароль login_data.password и user.hashed_password
    # Создаем токены access и refresh
    # Сохранить refresh_token в таблицу
    # Вернуть TokenResponse

    try:
        response = await http_client.verify_password(login_data.email, login_data.password)
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except UserServiceUnavailableError:
        raise HTTPException(status_code=503, detail="User service unavailable")
    except UserServiceError:
        raise HTTPException(status_code=500, detail="Internal server error")

    user_data = response.json()
    # Получаем Sub, username, email

    # Создаем токены
    access_token = create_access_token(
        user=user_data
    )
    refresh_token = create_refresh_token(
        user=user_data
    )

    # Сохраняем refresh_token в базу (если нужно)
    # ... код сохранения refresh_token ...

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )



# По сюда комментировал

# # Обновление access токена
# @router.post("/refresh", response_model=TokenResponse)
# async def refresh_token(
#         # session: AsyncSession,
#         refresh_token: RefreshTokenRequest,
# ):
#     # Сравнение token_data.type != "refresh" - ошиббка
#     # все ок - создаем токен новый
#     pass
#     # Обновляем access токен
#
#
# # Получение данных авторизованного пользователя
# @router.get("/users/me/", dependencies=[Depends(oauth2_scheme)])
# def auth_user_check_self_info(
#         payload: dict = Depends(get_current_token_payload),
#        # user: UserSchema = Depends(get_current_active_auth_user), # Этот метод для того, чтобы можно было проверять пользователя по token и public_key
# ):
#     iat = payload.get("iat")
#     jti = payload.get("jti")
#
#     # return {
#     #     "username": user.username,
#     #     "email": user.email,
#     #     "logged_in_at": iat,
#     #     "jti": jti,
#     # }
#     pass
#     # token = credentials.credentials
#     # payload = Проверка токена (token)
#     # Если payload.type != "access" - ошибка
#     # Если payload.sub нет, то не найден пользователь
#     # Вернуть UserInfo или UserData
#     # нужен эндпоинт для получения текущей сессии (то есть получения данных текущего пользователя)
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
# @router.get("/validate")
# async def validate_token(credentials: OAuth2PasswordRequestForm = Depends()):
#     # Проверяем токен
#     # Либо невалиден, либо
#     # return {"valid": True, "user_id": payload.sub}
#     pass
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