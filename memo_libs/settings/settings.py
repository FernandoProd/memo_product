from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn, RedisDsn, Field


class DatabaseConfig(BaseModel):
    """Database connection settings"""
    url: PostgresDsn
    echo: bool = Field(False, description="Echo SQL queries to stdout")
    echo_pool: bool = Field(False, description="Echo connection pool events")
    pool_size: int = Field(50, description="Number of connections to maintain in pool")
    max_overflow: int = Field(10, description="Maximum number of overflow connections")

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class RedisConfig(BaseModel):
    """Redis connection settings"""

    # move the url in the future
    url: RedisDsn = Field("redis://localhost:6379/0", description="Redis connection URL")
    socket_timeout: int = Field(5, description="Socket timeout in seconds")
    socket_connect_timeout: int = Field(5, description="Socket connect timeout in seconds")


class JWTConfig(BaseModel):
    """JWT settings"""
    pass


class GeneralSettings(BaseSettings):
    """
    General base class for all microservices
    You can use this class for inherit at your classes
    """

    # Nested configurations
    db: DatabaseConfig
    redis: RedisConfig = RedisConfig()
    # jwt: JWTConfig = JWTConfig()

    # CORS settings (move the urls to another place in the future)
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8001"
    ]


    # General application settings
    debug: bool = Field(False, description="Enable debug mode")
    environment: str = Field("development", description="Application environment")

    # For X-Internal-API-key
    internal_api_key: str = Field("", description="API key for internal services")

    # Services URLs
    user_service_url: str = Field("", description="URL for user service")
    auth_service_url: str = Field("", description="URL for auth service")

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        extra="ignore",
    )