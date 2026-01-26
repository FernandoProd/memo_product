from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

# api/v1/endpoints/auth.py
from pydantic import BaseModel

class UserData(BaseModel):
    username: str
    password: str
    email: str


@router.post("/register")
async def register_user(user_data: UserData):
    # Каким-то образом вызывается функция создания пользователя из user_service
    # Как-то пришпандоривается сюда пароль, которого почему-то нет в бд пользователя
    pass


@router.post("/login")
async def login():
    # 1. Проверяем в user_service (HTTP запрос)
    # 2. Создаем сессию в своей БД
    # 3. Возвращаем токены
    pass

@router.post("/refresh")
async def refresh_token():
    pass
    # Обновляем access токен

@router.post("/logout")
async def logout():
    # Инвалидируем сессию
    pass

@router.get("/verify")
async def verify_token(token: str):
    # Проверяем токен
    pass


def get_current_user():
    pass
    # нужен эндпоинт для получения текущей сессии (то есть получения данных текущего пользователя)


def update_user():
    pass
    # обновления логина и пароля