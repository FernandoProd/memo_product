Распределение эндпоинтов

auth_service (отвечает за аутентификацию и выдачу токенов):
- POST /login — принимает логин/пароль, проверяет их через user_service, выдаёт JWT/OAuth‑токен.
- POST /refresh — обновляет токен по refresh‑токену.
- POST /logout — аннулирует токен (или помещает в чёрный список).
- GET /whoami — возвращает данные о текущем пользователе (на основе токена).
- POST /validate-token — проверяет валидность токена (используется другими сервисами).

user_service (отвечает за управление пользователями):
- POST /users — регистрация нового пользователя (сохраняет хешированный пароль).
- GET /users/{id} — получение профиля пользователя.
- PUT /users/{id} — обновление профиля (email, имя и т. п.).
- DELETE /users/{id} — удаление аккаунта.
- POST /users/{id}/change-password — смена пароля (перехеширует и сохраняет).
- GET /users?search=... — поиск пользователей (для админов).


Решил использовать подход user-centric (регистрация через auth service)
Пользователь -> POST /user/register 
Но есть еще такой подход создания пользователя auth-centric


# **User Service Endpoints:**

## Пользователи:

text

POST    /users                         - Регистрация нового пользователя
POST    /users/verify-credentials      - Проверка логина/пароля (для auth service)
GET     /users/{user_id}              - Получение профиля пользователя
PUT     /users/{user_id}              - Обновление профиля
DELETE  /users/{user_id}              - Удаление пользователя
POST    /users/{user_id}/change-password - Смена пароля
GET     /users/{user_id}/password-hash - Получить хеш пароля (для синхронизации)
POST    /users/{user_id}/password-changed - Уведомление об изменении пароля
GET     /users                        - Поиск пользователей (админ)
GET     /users/by-username/{username} - Найти по username
GET     /users/by-email/{email}       - Найти по email

## Здоровье:

text

GET     /health                       - Проверка здоровья сервиса
GET     /health/db                    - Проверка подключения к БД

# **Auth Service Endpoints:**

## Аутентификация:

text

POST    /auth/login                   - Вход (получает токены)
POST    /auth/refresh                 - Обновление access токена
POST    /auth/logout                  - Выход (инвалидация токена)
POST    /auth/logout-all              - Выход со всех устройств

## Валидация:

text

POST    /auth/validate-token          - Проверка валидности токена
POST    /auth/introspect              - Подробная информация о токене
GET     /auth/me                      - Данные текущего пользователя

## Управление сессиями:

text

GET     /auth/sessions                - Получить все активные сессии
DELETE  /auth/sessions/{session_id}   - Завершить конкретную сессию

## Синхронизация (внутренние):

text

POST    /auth/sync/password           - Синхронизация пароля (от user service)
POST    /auth/sync/user-deleted       - Удаление кеша при удалении пользователя

## Здоровье:

text

GET     /health                       - Проверка здоровья сервиса
GET     /health/db                    - Проверка подключения к БД
GET     /health/cache                 - Статистика кеша паролей

## Кеш паролей (админка):

text

GET     /admin/password-cache         - Просмотр кеша
DELETE  /admin/password-cache/{user_id} - Удалить из кеша
POST    /admin/password-cache/sync    - Принудительная синхронизация

---

**Ключевое:**

- `user_service` — источник истины для данных пользователей
    
- `auth_service` — проверяет пароли через кеш, создает JWT токены
    
- Все запросы между сервисами защищены `X-API-Key`
    
- При смене пароля `user_service` уведомляет `auth_service`


