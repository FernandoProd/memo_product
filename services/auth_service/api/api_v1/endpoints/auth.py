from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.schemas import TokenResponse, LoginRequest, RefreshTokenRequest, LogoutRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])

# api/v1/endpoints/auth.py
from pydantic import BaseModel

class UserData(BaseModel):
    username: str
    password: str
    email: str


# Логин - получение токенов по login_data
@router.post("/login", response_model=TokenResponse)
async def login(
        session: AsyncSession,
        login_data: LoginRequest
):
    # user = get_user_by_email(session, login_data.email)
    # Если пользователя нет, то ошибка
    # Сравниваем хешированный пароль login_data.password и user.hashed_password
    # Создаем токены access и refresh
    # Сохранить refresh_token в таблицу
    # Вернуть TokenResponse
    pass

# Обновление access токена
@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
        session: AsyncSession,
        refresh_token: RefreshTokenRequest,
):
    # Сравнение token_data.type != "refresh" - ошиббка
    # все ок - создаем токен новый
    pass
    # Обновляем access токен

@router.get("/me", response_model=UserData)
async def get_current_user(
        # credentials: OAuth2PasswordRequestForm = Depends(security),
        session: AsyncSession,
):
    # token = credentials.credentials
    # payload = Проверка токена (token)
    # Если payload.type != "access" - ошибка
    # Если payload.sub нет, то не найден пользователь
    # Вернуть UserInfo или UserData
    pass
    # нужен эндпоинт для получения текущей сессии (то есть получения данных текущего пользователя)

# Выход (отзыв токена)
@router.post("/logout")
async def logout(
        session: AsyncSession,
        logout_request: LogoutRequest,
):
    # Если использую БД для refresh токенов
    # await revoke_refresh_token(session, logout_request.refresh_token)

    # Для stateless JWT - клиент просто удаляет токены
    # Инвалидируем сессию
    pass

@router.get("/validate")
async def validate_token(credentials: OAuth2PasswordRequestForm = Depends()):
    # Проверяем токен
    # Либо невалиден, либо
    # return {"valid": True, "user_id": payload.sub}
    pass

# @router
async def change_password(
        old_password: str,
        new_password: str,
        credentials: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(),
):
    pass

# @router
def update_user():
    pass
    # обновления логина и пароля

# dependency
# async get current user


#Для проверки ролей, но можно придумать и другие роли
# async get_current)admin_user



# 7. Использование в других сервисах:
# python
# # В user_service или других сервисах
# from fastapi import Depends
# from auth_service.core.dependencies import get_current_user
#
# @router.get("/protected")
# async def protected_route(
#     current_user: User = Depends(get_current_user)
# ):
#     return {"message": f"Hello {current_user.username}"}