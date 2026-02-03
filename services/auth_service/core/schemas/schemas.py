from pydantic import BaseModel, EmailStr


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class TokenResponse(BaseModel):
    access_token: str
    # refresh_token: str | None = None
    token_type: str = "Bearer"



class TokenData(BaseModel):
    pass


class LoginRequest(BaseModel):
    username: str
    email: str
    password: str


class LogoutRequest(BaseModel):
    pass


class RefreshTokenRequest(BaseModel):
    pass


class UserSchema(BaseModel):
    # model_config = ConfigDict(strict=True)
    sub: str
    username: str
    email: EmailStr | None = None
    roles: dict | None = None
    # is_active: bool = True


class RefreshTokenInfo(BaseModel):
    sub: str | bytes


class TokenInDBSchema(BaseModel):
    pass
