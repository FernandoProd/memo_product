from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from services.auth_service.utils import jwt_utils
from services.auth_service.core.schemas.schemas import UserSchema


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


def get_current_token_payload(
        # credentials: HTTPAuthorizationCredentials = Depends(http_bearer), #Вместо токена приходят credentials
        token: str = Depends(oauth2_scheme)
) -> UserSchema:
    # token = credentials.credentials
    # print(token)
    try:
        payload = jwt_utils.decode_jwt(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}"
        )

    return payload