from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: UUID
    is_active: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    # Nullable fields
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    deleted_at: Optional[datetime] = None

