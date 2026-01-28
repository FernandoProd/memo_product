from core.schemas.schemas import UserSchema

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

def create_jwt(
        token_type: str,
        token_data: dict,
) -> str:
    # jwt_payload = {
    #     TOKEN_TYPE_FIELD: token_type
    # }
    # jwt_payload.update(token_data)
    # return auth_utils.encode_jwt(
    #     payload=jwt_payload,
    #     expire_minutes=expire_minutes,
    #     expire_timedelta=expire_timedelta,
    # )
    pass

def create_access_token(
        user: UserSchema # По факту вызывается Endpoint verify из user_service
):
    jwt_payload = {
        "sub": user.user_id,
        "email": user.email,
        "username": user.username,
        "roles": user.roles,

    }