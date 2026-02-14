from sqlalchemy import MetaData
from memo_libs.database import CoreBase
from app.core.config import settings



class Base(CoreBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )
    # You can add some mixins to this class