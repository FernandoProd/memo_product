from sqlalchemy.orm import DeclarativeBase


class CoreBase(DeclarativeBase):
    __abstract__ = True

    # You can add common fields here if you need
    # You can add some common mixins to this class