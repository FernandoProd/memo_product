from datetime import timedelta

from services.auth_service.app.core.config import settings
from services.auth_service.app.utils.jwt_utils import encode_jwt


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

def create_jwt(
        token_type: str,
        token_data: dict,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
) -> str:
    """
    Create a JWT token with the given type and payload
    """

    jwt_payload = {TOKEN_TYPE_FIELD: token_type, **token_data}

    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )

def create_access_token(
        user: dict# UserSchema # По факту вызывается Endpoint verify из user_service
) -> str:
    """
    Create an access token for a user
    """

    jwt_payload = {
        "sub": user["sub"],
        "email": user["email"],
        "username": user["username"],
        "roles": user["roles"],
    }

    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes = settings.auth_jwt.access_token_expire_minutes,
    )


def create_refresh_token(user: dict) -> str:
    """
     Create a refresh token for a user.
    """

    jwt_payload = {
        "sub": user["sub"],
    }

    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    )