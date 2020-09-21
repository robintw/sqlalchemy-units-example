import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse

from model_basic import Base, ShipState

if os.path.exists("test.sqlite"):
    os.remove("test.sqlite")

engine = create_engine("sqlite:///test.sqlite")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Creating ShipState objects
state1 = ShipState(timestamp=parse("2020-01-01 10:13:34"), speed=15.4, distance=3048)
state2 = ShipState(timestamp=parse("2020-01-01 10:15:12"), speed=10.2, distance=2509)

print(f"State 1 speed = {state1.speed}")
print(f"State 2 distance = {state1.distance}")

session.add_all([state1, state2])
session.commit()
