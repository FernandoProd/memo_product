from sqlalchemy.ext.asyncio import AsyncSession
from services.auth_service.app.models import RefreshToken
from sqlalchemy import select, update


async def add_token(
        session: AsyncSession,
        token_data: RefreshToken
):
    session.add(token_data)
    await session.commit() # Можно делать его делать на уровень выше, чтобы помещать в ттранзакцию больше функционала
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


async def revoke_token(
        session: AsyncSession,
        hashed_refresh_token: str
) -> bool:
    stmt = (
        update(RefreshToken)
        .where(
            RefreshToken.token_hash == hashed_refresh_token,
            RefreshToken.revoked == False
        )
        .values(revoked=True)
        .execution_options(synchronize_session="fetch")
    )

    result = await session.execute(stmt)
    if result.rowcount == 0:
        raise ValueError("Refresh token not found or already revoked")

    await session.commit() # Можно делать на уровень выше

    return True