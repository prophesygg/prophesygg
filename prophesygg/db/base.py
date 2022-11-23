from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.sql import text

from sqlalchemy.dialects.mysql import TIMESTAMP


class ProphesyModel:
    """
    ProphesyModel should be the parent class for every Prophesy data model. Created/Updated columns are automatically added.
    """

    __tablename__ = None
    Created = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    Updated = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )


ProphesyBase: DeclarativeMeta = declarative_base(cls=ProphesyModel)
