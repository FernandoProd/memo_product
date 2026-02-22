from sqlalchemy.ext.asyncio import AsyncSession

from services.auth_service.app.crud.tokens import get_refresh_token, revoke_token
from services.auth_service.app.models import RefreshToken
from datetime import datetime
from services.auth_service.app.utils.jwt_utils import decode_jwt
from services.auth_service.app.core.security.utils import hash_token
from services.auth_service.app.crud import tokens

class AuthService:
    async def add_token_info_into_db(
            self,
            session: AsyncSession,
            refresh_token: str,
    ) -> RefreshToken:
        payload = decode_jwt(token=refresh_token)
        user_id = payload.get("sub")
        # iat_timestamp = payload.get("iat")
        exp_timestamp = payload.get("exp")
        # issued_at = datetime.utcfromtimestamp(iat_timestamp).strftime('%Y-%m-%d %H:%M:%S UTC') if iat_timestamp else None
        expires_at = datetime.utcfromtimestamp(exp_timestamp)

        hashed_token = hash_token(refresh_token)
        token_data = RefreshToken(
            user_id=user_id,
            token_hash=hashed_token,
            expires_at=expires_at,
        )

        added_token = await tokens.add_token(
            session=session,
            token_data=token_data,
        )
        # session.add(token_model)
        # await session.commit()
        return token_data

    async def refresh_token_into_db(
            self,
            session: AsyncSession,
            refresh_token: str,
    ) -> bool:
        try:
            hashed_token = hash_token(refresh_token)
            check_token = await get_refresh_token(session, hashed_token)
            if check_token:
                return True
            return False
        except Exception as e:
            raise e

    async def revoke_refresh_token(
            self,
            session: AsyncSession,
            refresh_token: str,
    ):
        try:
            hashed_token = hash_token(refresh_token)
            revoked = await revoke_token(session, hashed_token)
            if revoked:
                return True
            return False
        except Exception as e:
            raise e
