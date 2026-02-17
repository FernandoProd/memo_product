from pathlib import Path
from pydantic import BaseModel, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from memo_libs.settings import GeneralSettings, RedisConfig
import logging


logger = logging.getLogger(__name__)

AUTH_SERVICE_DIR = Path(__file__).parent.parent.parent # services/auth_service
BASE_DIR = AUTH_SERVICE_DIR.parent.parent # memo_product

class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8001

class AuthJWT(BaseModel):
    private_key_path: Path = AUTH_SERVICE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = AUTH_SERVICE_DIR/ "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 5
    refresh_token_expire_days: int = 30


# class DatabaseConfig(BaseModel):
#     url: PostgresDsn
#     echo: bool = False
#     echo_pool: bool = False
#     pool_size: int = 50
#     max_overflow: int = 10
#
#     naming_convention: dict[str, str] = {
#         "ix": "ix_%(column_0_label)s",
#         "uq": "uq_%(table_name)s_%(column_0_name)s",
#         "ck": "ck_%(table_name)s_%(constraint_name)s",
#         "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#         "pk": "pk_%(table_name)s",
#     }

class AuthRedisConfig(RedisConfig):
    # REDIS_HOST: str = "localhost"  # перенести чтение на .env файл
    # REDIS_PORT: int = 6379
    # REDIS_DB: int = 0
    # REDIS_PASSWORD: str = "redis"
    url: RedisDsn = "redis://localhost:6379/0"


class Settings(GeneralSettings):
    # Service specific settings
    run: RunConfig = RunConfig()
    auth_jwt: AuthJWT = AuthJWT()
    # api: ApiPrefix = ApiPrefix()
    redis: AuthRedisConfig = AuthRedisConfig()

    model_config = {
        **GeneralSettings.model_config,
        "env_file": (
            AUTH_SERVICE_DIR / ".env.template",
            AUTH_SERVICE_DIR / ".env",
        ),
        "case_sensitive": False,  # Переменные окружения будут читаться без учета регистра
    }
    logger.debug("Вот, что выводится в model_config: %s", model_config)


settings = Settings()
logger.info("Успешно начали отладку!")
print("PostrgeURL: ", settings.db.url)
print("Echo: ", settings.db.echo)
print("JWT private key path: ", settings.auth_jwt.private_key_path)
print("JWT public key path: ", settings.auth_jwt.public_key_path)
print("JWT algorithm: ", settings.auth_jwt.algorithm)
print("redis test: ", settings.redis.url)
