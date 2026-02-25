from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from services.auth_service.app.utils import jwt_utils
from services.auth_service.app.schemas.schemas import UserSchema


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")

def get_current_token_payload(
        token: str = Depends(oauth2_scheme)
) -> UserSchema:
    try:
        payload = jwt_utils.decode_jwt(token)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}"
        )

    return payload


def verify_users_token(token: str):
    try:
        payload = jwt_utils.decode_jwt(token)
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )



