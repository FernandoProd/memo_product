from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn, RedisDsn
# from pathlib import Path

# USER_SERVICE_DIR = Path(__file__).parent.parent

# class RunConfig(BaseModel):
#     host: str = "0.0.0.0"
#     port: int = 8000
#
#
# class ApiV1Prefix(BaseModel):
#     prefix: str = "/v1"
#     users: str = "/users"


# class ApiPrefix(BaseModel):
#     prefix: str = "/api"
#     v1: ApiV1Prefix = ApiV1Prefix()


class DatabaseConfig(BaseModel):
    """Database connection settings"""
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class RedisConfig(BaseModel):
    """Redis connection settings"""
    url: RedisDsn = "redis://localhost:6379/0"
    socket_timeout: int = 5
    socket_connect_timeout: int = 5


# Разобраться для чего выносить jwt конфиг в общий файл
class JWTConfig(BaseModel):
    """JWT settings"""
    secret_key: str = "change_me_in_production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7



class GeneralSettings(BaseSettings):
    """
    General base class for all microservices
    You can use this class for inherit at your classes
    """

    # Nested configurations
    db: DatabaseConfig
    redis: RedisConfig = RedisConfig()
    jwt: JWTConfig = JWTConfig()


    # CORS (can be overridden per service) (how can I use it?)
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]


    # General (how can I use it?)
    debug: bool = False
    environment: str = "development"

    model_config = SettingsConfigDict(
       # env_file=(
       #     SERVICE_DIR / ".env.template",
       #     SERVICE_DIR / ".env",        # Не указываем путь, так как в каждом классе он мудет специфичен
       # ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        # extra="ignore",     # Что это дает?
    )


# settings = Settings()
# print(settings.db.url)
# print(settings.db.echo)