#
# Example code from 'Pint + SQLAlchemy = Unit consistency and enforcement in your database' poster
# at PyData Global 2020
# by Robin Wilson (robin@rtwilson.com)
#
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse

from model_basic import Base, ShipState

# Remove the db file if it already exists
if os.path.exists("test.sqlite"):
    os.remove("test.sqlite")

# Create a SQLite engine to connect to the database, and create the tables
engine = create_engine("sqlite:///test.sqlite")
Base.metadata.create_all(engine)

# Create a session object
Session = sessionmaker(bind=engine)
session = Session()

# Creating ShipState objects
state1 = ShipState(timestamp=parse("2020-01-01 10:13:34"), speed=15.4, distance=3048)
state2 = ShipState(timestamp=parse("2020-01-01 10:15:12"), speed=10.2, distance=2509)

print(f"State 1 speed = {state1.speed}")
print(f"State 2 distance = {state1.distance}")

session.add_all([state1, state2])
session.commit()
