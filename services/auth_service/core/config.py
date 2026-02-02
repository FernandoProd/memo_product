from pathlib import Path
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings
from pydantic import Field

BASE_DIR = Path(__file__).parent.parent

class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8001

class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 5
    refresh_token_expire_days: int = 30


class DatabaseConfig(BaseModel):
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

class RedisDBConfig(BaseModel):
    REDIS_HOST: str = "localhost"  # перенести чтение на .env файл
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = "redis"

class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    USER_SERVICE_URL: str = Field(
        default="http://localhost:8001",  # Значение по умолчанию (Значение в env.template еще включено) надо добавить
        description="URL auth service"
    )
    run: RunConfig = RunConfig()
    db: DatabaseConfig


settings = Settings()