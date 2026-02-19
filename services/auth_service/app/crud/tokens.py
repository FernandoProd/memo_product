from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from services.auth_service.app.models import RefreshToken
from sqlalchemy import select

# def get_token_lifetime_info(token: str) -> dict:
#     """
#     Возвращает дату выдачи и окончания срока действия JWT-токена.
#     """
#     payload = decode_jwt(token=token)
#
#     iat_timestamp = payload.get("iat")
#     exp_timestamp = payload.get("exp")
#
#     issued_at = datetime.utcfromtimestamp(iat_timestamp).strftime('%Y-%m-%d %H:%M:%S UTC') if iat_timestamp else None
#     expires_at = datetime.utcfromtimestamp(exp_timestamp).strftime('%Y-%m-%d %H:%M:%S UTC') if exp_timestamp else None
#
#     return {
#         "issued_at": issued_at,
#         "expires_at": expires_at,
#         "is_expired": exp_timestamp < datetime.utcnow().timestamp() if exp_timestamp else None
#     }



# async def add_token_info_into_db(
#         session: AsyncSession,
#         refresh_token: str,
# ) -> RefreshToken:
#     payload = decode_jwt(token=refresh_token)
#     user_id = payload.get("sub")
#     # iat_timestamp = payload.get("iat")
#     exp_timestamp = payload.get("exp")
#     # issued_at = datetime.utcfromtimestamp(iat_timestamp).strftime('%Y-%m-%d %H:%M:%S UTC') if iat_timestamp else None
#     expires_at = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
#
#
#
#     hashed_token = hash_token(refresh_token)
#     token_model = RefreshToken(
#         user_id=user_id,
#         token_hash=str(hashed_token),
#         expires_at=expires_at,
#     )
#     session.add(token_model)
#     await session.commit()
#     return token_model


async def add_token(
        session: AsyncSession,
        token_data: RefreshToken
):
    session.add(token_data)
    await session.commit()
    return token_data


async def get_refresh_token(
        session: AsyncSession,
        hashed_refresh_token: str
) -> RefreshToken:
    try:
        stmt = select(RefreshToken).where(
            RefreshToken.token_hash == hashed_refresh_token,
            RefreshToken.revoked == False
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    except Exception as e:
        raise e


async def get_user_id_by_token_hash():
    pass