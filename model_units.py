#
# Example code from 'Pint + SQLAlchemy = Unit consistency and enforcement in your database' poster
# at PyData Global 2020
# by Robin Wilson (robin@rtwilson.com)
#
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime, Integer, Column
from sqlalchemy.dialects.sqlite import REAL
from sqlalchemy.ext.hybrid import hybrid_property
from pint import UnitRegistry

# As usual, create the 'Base' object for all SQLAlchemy models to inherit from
Base = declarative_base()
# Create the 'unit registry' which holds all the details of the pint units
unit_registry = UnitRegistry()


# This class has got a bit more complicated this time - but we'll go through it step by step
class ShipState(Base):
    __tablename__ = "ShipStates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    # Note that the speed and distance instance variables are now renamed to _speed and _distance
    # but we pass the name we want the column in the db to use as the first argument
    # so the columns in the db are still called "speed" and "distance"
    _speed = Column("speed", REAL)
    _distance = Column("distance", REAL)

    # The hybrid_property decorator is key to this, it defines a property that behaves in different
    # ways when used in different places in SQLAlchemy
    @hybrid_property
    def speed(self):
        # The function here is the 'getter', called when we read a value on the object
        # This returns all speeds as metres per second

        # Have to check for None's as pint doesn't deal with None values having units
        if self._speed is None:
            return None
        else:
            # They are stored in m/s in the database (though just as a float)
            # so we just assign the units here to the value we got out of the database
            return self._speed * (unit_registry.metre / unit_registry.second)

    @speed.setter
    def speed(self, speed):
        # The function here is the 'setter', called when we set a value on the object

        # Again, deal with None values
        if speed is None:
            self._speed = None
            return

        # Check the given speed is a pint.Quantity instance with a dimension of 'length / time'
        # This is how a speed is defined - it's a certain measure of length (eg. metres) divided by a certain
        # measure of time (eg. seconds)
        try:
            if not speed.check("[length]/[time]"):
                # Raise an error if it's got a different dimensionality
                raise ValueError(
                    "Speed must be a Quantity with a dimensionality of [length]/[time]"
                )
        except AttributeError:
            # Raise an error if it has no units at all (ie. is not a Quantity)
            raise TypeError("Speed must be a Quantity")

        # Set the actual speed attribute to the given value converted to metres per second
        self._speed = speed.to(unit_registry.metre / unit_registry.second).magnitude

    @speed.expression
    def speed(self):
        # This is the function called when a column is used as a filter in a SQLAlchemy query.
        # The SQLAlchemy query engine has to know how to convert whatever is returned here
        # into something that the db backend understands, so here we just return a float value
        # in metres per second (just as stored in the db). We could do conversions here to return values
        # in a different unit to the value stored in the database.
        return self._speed

    ####################################################
    ####################################################

    # The code below has the hybrid properties for the distance column
    # They follow the same pattern as above, but check for a different dimensionality

    @hybrid_property
    def distance(self):
        # Return all distances as metres
        if self._distance is None:
            return None
        else:
            return self._distance * unit_registry.metre

    @distance.setter
    def distance(self, distance):
        if distance is None:
            self._distance = None
            return

        # Check the given distance is a Quantity with a dimension of 'length'
        try:
            if not distance.check("[length]"):
                raise ValueError("distance must be a Quantity with a dimensionality of [length]")
        except AttributeError:
            raise TypeError("distance must be a Quantity")

        # Set the actual distance attribute to the given value converted to metres
        self._distance = distance.to(unit_registry.metre).magnitude

    @distance.expression
    def distance(self):
        return self._distance
