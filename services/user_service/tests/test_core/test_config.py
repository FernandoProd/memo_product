# Импортируем настройки
from app.core.config import Settings


def test_settings_can_be_created_with_env_file():
    """Проверяем, что настройки загружаются из .env файла"""
    settings = Settings(_env_file="services/user_service/.env.template")

    assert settings.db.echo == True
    assert str(settings.db.url) == "postgresql+asyncpg://user:password@localhost:5433/user"
    # assert settings.run.host == "0.0.0.0"
    # assert settings.run.port == 8000
    # assert settings.api.prefix == "/api"
    # assert settings.api.v1.prefix == "/v1"
    # assert settings.api.v1.users == "/users"