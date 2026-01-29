from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic import Field

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 5
    refresh_token_expire_days: int = 30


class Settings(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()
    USER_SERVICE_URL: str = Field(
        default="http://localhost:8001",  # Значение по умолчанию (Значение в env.template еще включено) надо добавить
        description="URL users service"
    )


settings = Settings()