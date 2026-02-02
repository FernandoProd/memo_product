from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import String, Boolean, Index
from services.auth_service.core.models.base import Base
import datetime


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),  # Используем PostgreSQL UUID тип
        primary_key=True,
        default=uuid.uuid4,  # Автогенерация UUID
        index=True,
        unique=True
    )

    user_id: Mapped[str] = mapped_column(
        String(36),
        nullable=False,
        index=True
    )

    token_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
        index=True
    )  # SHA256 хеш

    expires_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False,
        index=True
    )

    # Надо ли это добавлять если инфа есть в самих токенах
    # expires_at: Mapped[datetime] =   ДЛЯ ОЧИСТКИ
    # created_at: Mapped[datetime] =   ДЛЯ АНАЛИТИКИ
    revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        index=True)

    device_id: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        index=True
    )

    # Составные индексы для частых запросов:
    __table_args__ = (
        Index('ix_user_revoked_expires', 'user_id', 'revoked', 'expires_at'), # индекс для быстрого поиска активных токенов по user_id и revoked.
    )


# Модель для rate limiting и безопасности
# class AuthAttempt(Base):
#     __tablename__ = "auth_attempts"
#
#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     user_id = Column(String(36), nullable=True, index=True)  # null если пользователь не найден
#     email = Column(String(255), nullable=False, index=True)
#     ip_address = Column(String(45), nullable=False, index=True)
#     user_agent = Column(String(512), nullable=True)
#     success = Column(Boolean, default=False)
#     created_at = Column(DateTime, default=datetime.utcnow, index=True)
#
#     __table_args__ = (
#         Index('ix_auth_attempts_ip_time', 'ip_address', 'created_at'),
#         Index('ix_auth_attempts_email_time', 'email', 'created_at'),
#     )