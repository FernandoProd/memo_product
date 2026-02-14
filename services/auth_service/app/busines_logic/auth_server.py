from sqlalchemy.ext.asyncio import AsyncSession
from app.models import RefreshToken
from datetime import datetime
from app.utils.jwt_utils import decode_jwt
from app.core.security.utils import hash_token
from app.crud import tokens

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