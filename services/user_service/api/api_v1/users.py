from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from core.busines_logic.user import UserService
from core.models import db_helper
from core.schemas.user import UserCreate, UserRead
from crud import users as users_crud

router = APIRouter(tags=["Users"])

@router.post("", response_model=UserRead)
async def create_user(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter)
        ],
        user_data: UserCreate,
):
    service = UserService()
    user = await service.create_user_with_hash(
        session=session,
        user_data=user_data,
    )
    return user