'''
Module containing the database set-up
'''

# Import dependencies
import os
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# Base definition
Base = declarative_base()

# Create engine
#dbpath = os.path.join('db', 'pets.sqlite')
dbpath = os.path.join('db','belly_button_biodiversity.sqlite')
engine = create_engine(f'sqlite:///{dbpath}')

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# assign otu table to variable
otu_variable = Base.classes.otu

# assign samples table to variable
Sample = Base.classes.samples

# assign samples_metadata table to variable
meta = Base.classes.samples_metadata

# Create a session
session = Session(engine)








