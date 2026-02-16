import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column
from services.user_service.app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),  # Используем PostgreSQL UUID тип
        primary_key=True,
        default=uuid.uuid4,  # Автогенерация UUID
        index=True,
        unique=True
    )

    """login identifiers"""
    username: Mapped[str] = mapped_column(
        String(50),  # Ограничение длины
        unique=True,
        index=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),  # Стандартная длина для email
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    """more information"""
    first_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    last_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    """Another fields"""
    display_name: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    """image maybe"""
    avatar_url: Mapped[Optional[str]] = mapped_column(
        String(500),  # URL может быть длинным
        nullable=True
    )

    """Status and metadata"""
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False
    )

    is_deleted: Mapped[bool] = mapped_column(
        default=False,  # Soft delete флаг
        nullable=False
    )

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,  # Используем UTC время
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,  # Автообновление при изменении
        nullable=False
    )













# # API Gateway получает запрос регистрации
# POST /auth/register
#
# # API Gateway вызывает:
# # 1. Сначала User Service
# POST /internal/users
# {
#     "username": "john_doe",
#     "email": "john@example.com",
#     "first_name": "John",
#     "last_name": "Doe"
# }
# # Возвращает user_id
#
# # 2. Затем Auth Service
# POST /internal/auth/credentials
# {
#     "user_id": "полученный_user_id",
#     "username": "john_doe",
#     "email": "john@example.com",
#     "password": "secure123"
# }
#
# # 3. Возвращает клиенту токен