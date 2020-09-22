# Pint + SQLAlchemy example code

This repo contains the example code that goes with the _Pint + SQLAlchemy = Unit consistency and enforcement in your database_ poster at PyData Global 2020.

To use:

1. Install the dependencies with `pip install -r requirements.txt`.

2. Look at [model_basic.py](model_basic.py) and [demo_basic.py](demo_basic.py) which show standard SQLAlchemy code to define a simple model and use it to insert a couple of rows into a database table. Nothing in these files is novel - this is standard SQLAlchemy usage. Running `demo_basic.py` will print out a bit of information about the rows inserted.

3. Look at [model_units.py](model_units.py) to see how the model has been changed to check and enforce units, and then [demo_units.py](demo_units.py) to see how to use the new model. Running `demo_units.py` will show the values at various stages, showing that unit conversion and enforcement has happened. Uncomment some of the commented lines in `demo_units.py` to see what happens when you try and give a value with incorrect units.

Please feel free to contact me on robin@rtwilson.com with any questions - I will endeavour to get back to you as soon as I can.
