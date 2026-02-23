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
    prefix: str = "/v1"
    users: str = "/users"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class Settings(GeneralSettings):
    # Service specific settings
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()

    # internal_api_key: str =

    model_config = {
        **GeneralSettings.model_config,
        "env_file": (
            USER_SERVICE_DIR / ".env.template",
            USER_SERVICE_DIR / ".env",
        ),
        "case_sensitive": False,  # Переменные окружения будут читаться без учета регистра
    }
    logger.debug("Вот, что выводится в model_config: %s", model_config)


settings = Settings()
logger.info("Успешно начали отладку!")
print("PostrgeURL: ", settings.db.url)
print("Echo: ", settings.db.echo)
print("Internal API key:", settings.internal_api_key)
# print("JWT secret key: ", settings.jwt.secret_key)

#http://127.0.0.1:8000/docs