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
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        unique=True
    )

    """login identifiers"""
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
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
        String(500),
        nullable=True
    )

    """Status and metadata"""
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False
    )

    is_deleted: Mapped[bool] = mapped_column(
        default=False,
        nullable=False
    )

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


