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
    id: int

