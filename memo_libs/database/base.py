from sqlalchemy.orm import DeclarativeBase


class CoreBase(DeclarativeBase):
    """Base class for all database models"""

    __abstract__ = True

    # You can add common fields here (id, created_at, updated_at)
    # You can add some common mixins to this class