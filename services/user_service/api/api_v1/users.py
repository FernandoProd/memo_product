from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

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
        user_create: UserCreate,
):
    user = await users_crud.create_user(
        session=session,
        user_create=user_create,
    )
    return user