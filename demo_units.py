#
# Example code from 'Pint + SQLAlchemy = Unit consistency and enforcement in your database' poster
# at PyData Global 2020
# by Robin Wilson (robin@rtwilson.com)
#
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dateutil.parser import parse

from model_units import Base, ShipState, unit_registry

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

# Examples of correct units for speed
state1 = ShipState(timestamp=parse("2020-01-01 10:13:34"), speed=15.4 * unit_registry.knot)
state2 = ShipState(
    timestamp=parse("2020-01-01 10:15:12"),
    speed=10.2 * (unit_registry.miles / unit_registry.hours),
)
state3 = ShipState(
    timestamp=parse("2020-01-01 10:15:12"),
    speed=10.2 * (unit_registry.angstrom / unit_registry.year),
)

# Examples of correct units for distance
state4 = ShipState(timestamp=parse("2020-01-01 10:13:34"), distance=3048 * unit_registry.yards)
state5 = ShipState(timestamp=parse("2020-01-01 10:15:12"), distance=19.2 * unit_registry.km)
state6 = ShipState(timestamp=parse("2020-01-01 10:15:12"), distance=0.02 * unit_registry.lightyear)

# Examples of incorrect units or missing units
# These will all raise exceptions if commented out
#
# invalid_state = ShipState(timestamp=parse('2020-01-01 10:13:34'), speed=15.4)
# invalid_state = ShipState(timestamp=parse('2020-01-01 10:13:34'), speed=15.4 * unit_registry.hour)
# invalid_state = ShipState(timestamp=parse('2020-01-01 10:13:34'), speed=15.4 * (unit_registry.metre / unit_registry.degree))
# invalid_state = ShipState(timestamp=parse('2020-01-01 10:13:34'), distance=10 * unit_registry.newton)
# invalid_state = ShipState(timestamp=parse('2020-01-01 10:13:34'), distance=10 * unit_registry.tonne)

# Printing values shows all speeds have been converted to metres per second
# but can easily be converted to any other valid unit
print(f"State 1 speed = {state1.speed}")
print(f"State 1 speed (in knots) = {state1.speed.to(unit_registry.knot)}")
print(f"State 2 speed = {state2.speed}")
print(f"State 3 speed = {state3.speed}")

# and all distances have been converted to metres
print(f"State 4 distance = {state4.distance}")
print(f"State 4 distance (in yards) = {state4.distance.to(unit_registry.yards)}")
print(f"State 5 distance = {state5.distance}")
print(f"State 6 distance = {state6.distance}")

# Adding the objects to the database works as normal - as internally all the Quantity objects
# have been converted to floats in metres per second, and the database can deal with them
session.add_all([state1, state2, state3, state4, state5, state6])
session.commit()

# Now we query for a distance of < 3000. All querying takes place in the database units, so
# in this case it is in metres per second
results = session.query(ShipState).filter(ShipState.distance < 3000).all()
print(f"Query result: state.distance = {results[0].distance}")
