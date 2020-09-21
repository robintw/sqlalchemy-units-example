#
# Example code from 'Pint + SQLAlchemy = Unit consistency and enforcement in your database' poster
# at PyData Global 2020
# by Robin Wilson (robin@rtwilson.com)
#

# To understand this you will need to understand the basics of SQLAlchemy - try following
# this tutorial first if you're unsure: https://docs.sqlalchemy.org/en/13/orm/tutorial.html

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime, Integer, Column
from sqlalchemy.dialects.sqlite import REAL

# As usual, create the 'Base' object for all SQLAlchemy models to inherit from
Base = declarative_base()


# Simple SQLAlchemy class definition with four columns
class ShipState(Base):
    __tablename__ = "ShipStates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    speed = Column(REAL)
    distance = Column(REAL)
