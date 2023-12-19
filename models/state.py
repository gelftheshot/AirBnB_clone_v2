#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """
    Represents a state in the application.

    Attributes:
        name (str): The name of the state.
        cities (list): A list of City objects associated with the state.
    """
    __tablename__ = "states"
    if models.storage_type == "db":
        name = Column(String(128), nullable=False)
        cities = relationship(
            "City", backref="state", cascade="all, delete, delete-orphan"
        )
    else:
        name = ""

        @property
        def cities(self):
            """
            Retrieves all cities associated with the current state.

            Returns:
                A list of City objects.
            """
            city_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
