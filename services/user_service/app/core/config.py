from pydantic import BaseModel
from libs.settings import GeneralSettings
from pathlib import Path

USER_SERVICE_DIR = Path(__file__).parent.parent.parent # Корень user_service

class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


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

    model_config = GeneralSettings.model_config.copy()
    model_config["env_file"](
       env_file=(
           USER_SERVICE_DIR / ".env.template",
           USER_SERVICE_DIR / ".env",
       ),
        case_sensitive=False, # Что это делает?
        # env_nested_delimiter="__",
        # env_prefix="APP_CONFIG__",
    )


settings = Settings()
# print(settings.db.url)
# print(settings.db.echo)
# print(settings.jwt.secret_key)

#http://127.0.0.1:8000/docs