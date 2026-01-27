from pydantic import BaseModel


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class TokenResponse(BaseModel):
    pass


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