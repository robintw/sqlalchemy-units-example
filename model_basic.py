from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime, Integer, Column
from sqlalchemy.dialects.sqlite import REAL


Base = declarative_base()


class ShipState(Base):
    __tablename__ = "ShipStates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    speed = Column(REAL)
    distance = Column(REAL)
