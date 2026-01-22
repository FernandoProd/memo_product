import pytest
import os
from pathlib import Path
from unittest.mock import patch

# Импортируем настройки
from services.user_service.core.config import Settings, DatabaseConfig


def test_settings_can_be_created_with_env_file():
    """Проверяем, что настройки загружаются из .env файла"""
    settings = Settings(_env_file="services/user_service/.env.template")

    assert settings.db.echo == True
    assert str(settings.db.url) == "postgresql+asyncpg://user:pwd@localhost:5433/app"
    # assert settings.run.host == "0.0.0.0"
    # assert settings.run.port == 8000
    # assert settings.api.prefix == "/api"
    # assert settings.api.v1.prefix == "/v1"
    # assert settings.api.v1.users == "/users"