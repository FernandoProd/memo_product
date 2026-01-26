Решил использовать подход auth-centric (регистрация через auth service)
Пользователь -> POST /auth/register -> auth_service -> создает в user-service
Но есть еще такой подход создания пользователя User-centric

POST /auth/register
{
    "username": "john",
    "email": "john@example.com",
    "password": "secure123",
    "first_name": "John",
    "last_name": "Doe"
}

# 2. Логин
POST /auth/login
{
    "username": "john",
    "password": "secure123"
}
# Возвращает: {access_token, refresh_token, token_type, expires_in}

# 3. Обновление токена
POST /auth/refresh
{
    "refresh_token": "xxxxx"
}

# 4. Выход
POST /auth/logout
Authorization: Bearer <token>

# 5. Проверка токена
GET /auth/verify?token=xxxxx
# или
POST /auth/introspect
{
    "token": "xxxxx"
}
# Возвращает: {valid: true, user_id: "uuid", scopes: [...]}

# 6. Смена пароля (требует аутентификации)
POST /auth/change-password
Authorization: Bearer <token>
{
    "old_password": "old123",
    "new_password": "new456"
}

# 7. Восстановление пароля
POST /auth/forgot-password
{
    "email": "john@example.com"
}

POST /auth/reset-password
{
    "token": "reset_token_from_email",
    "new_password": "new123"
}


