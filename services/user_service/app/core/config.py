from pathlib import Path
from pydantic import BaseModel, Field
from memo_libs.settings import GeneralSettings
import logging


logger = logging.getLogger(__name__)


USER_SERVICE_DIR = Path(__file__).parent.parent.parent          # services/user_service


class RunConfig(BaseModel):
    """Development server settings"""
    host: str = Field("0.0.0.0", description="Bind host")
    port: int = Field(8000, description="Bind port")


class ApiV1Prefix(BaseModel):
    """API v1 prefix settings"""
    prefix: str = Field("/v1", description="Base prefix for v1 endpoints")
    users: str = Field("/users", description="Prefix for users endpoints")


class ApiPrefix(BaseModel):
    """API prefix settings"""
    prefix: str = Field("/api", description="Base API prefix")
    v1: ApiV1Prefix = ApiV1Prefix()


class Settings(GeneralSettings):
    """
    User service specific settings.
    Inherits common configuration from GeneralSettings and adds service-specific fields.
    """

    # Service specific settings
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()

    # Override base model configuration to add env file support
    model_config = {
        **GeneralSettings.model_config,
        "env_file": (
            USER_SERVICE_DIR / ".env.template",
            USER_SERVICE_DIR / ".env",
        ),
        "case_sensitive": False,     # will be read without case
    }
    logger.debug("Вот, что выводится в model_config: %s", model_config)


# Global settings instance
settings = Settings()


# Log successful configuration load (without sensitive data)
logger.info(
    "Configuration loaded successfully. Environment: %s, Debug: %s",
    settings.environment,
    settings.debug,
)

print("PostrgeURL: ", settings.db.url)
print("Echo: ", settings.db.echo)
print("Internal API key:", settings.internal_api_key)
print("User service URL: ", settings.user_service_url)
print("Auth service URL: ", settings.user_service_url)
# print("JWT secret key: ", settings.jwt.secret_key)

#http://127.0.0.1:8000/docs