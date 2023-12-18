#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String, ForeignKey


class City(BaseModel, Base):
    """
    City class represents a city in the AirBnB clone v2 project.

    Attributes:
        __tablename__ (str): The name of the database table for cities.
        state_id (str): The ID of the state that the city belongs to.
        name (str): The name of the city.
    """
    __tablename__ = "cities"
    if storage_type == "db":
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
    else:
        state_id = ""
        name = ""
