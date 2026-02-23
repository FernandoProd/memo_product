from pathlib import Path
from pydantic import BaseModel, Field
from memo_libs.settings import GeneralSettings
import logging


logger = logging.getLogger(__name__)


AUTH_SERVICE_DIR = Path(__file__).parent.parent.parent          # services/auth_service
BASE_DIR = AUTH_SERVICE_DIR.parent.parent                       # memo_product

class RunConfig(BaseModel):
    """Development server settings"""
    host: str = Field("0.0.0.0", description="Bind host")
    port: int = Field(8001, description="Bind port")

class AuthJWTConfig(BaseModel):
    """JWT authentication settings specific to auth service"""

    private_key_path: Path = Field(
        default=AUTH_SERVICE_DIR / "certs" / "jwt-private.pem",
        description="Path to private key for signing tokens"
    )
    public_key_path: Path = Field(
        default=AUTH_SERVICE_DIR / "certs" / "jwt-public.pem",
        description="Path to public key for verifying tokens"
    )
    algorithm: str = Field("RS256", description="JWT signing algorithm")
    access_token_expire_minutes: int = Field(5, description="Access token TTL in minutes")
    refresh_token_expire_days: int = Field(30, description="Refresh token TTL in days")


class Settings(GeneralSettings):
    """
    Auth service specific settings.
    Inherits common configuration from GeneralSettings and adds service-specific fields.
    """

    # Service specific settings
    run: RunConfig = RunConfig()
    auth_jwt: AuthJWTConfig = AuthJWTConfig()
    # api: ApiPrefix = ApiPrefix()

    # Override base model configuration to add env file support
    model_config = {
        **GeneralSettings.model_config,
        "env_file": (
            AUTH_SERVICE_DIR / ".env.template",
            AUTH_SERVICE_DIR / ".env",
        ),
        "case_sensitive": False,
    }


# Global settings instance
settings = Settings()


print("PostrgeURL: ", settings.db.url)
print("Echo: ", settings.db.echo)
print("JWT private key path: ", settings.auth_jwt.private_key_path)
print("JWT public key path: ", settings.auth_jwt.public_key_path)
print("JWT algorithm: ", settings.auth_jwt.algorithm)
print("JWT algorithm: ", settings.auth_jwt.access_token_expire_minutes)
print("JWT algorithm: ", settings.auth_jwt.refresh_token_expire_days)
print("redis test: ", settings.redis.url)
print("Redis socket timeout: ", settings.redis.socket_timeout)