#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import models
from datetime import datetime
from sqlalchemy import Column, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(
        String(60), nullable=False, primary_key=True, unique=True
    )
    created_at = Column(
        DATETIME, nullable=False, default=datetime.utcnow()
    )
    updated_at = Column(
        DATETIME, nullable=False, default=datetime.utcnow()
    )

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for attr, value in kwargs.items():
                if attr in ["created_at", "updated_at"]:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if attr != "__class__":
                    setattr(self, attr, value)

            if models.storage_type == "db":
                if "id" not in kwargs:
                    self.id = str(uuid.uuid4())

                if "created_at" not in kwargs:
                    self.created_at = datetime.now()

                if "updated_at" not in kwargs:
                    self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split(".")[-1]).split("'")[0]
        return "[{}] ({}) {}".format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({"__class__": (str(type(self)).split(".")[-1]).split("'")[0]})
        dictionary["created_at"] = self.created_at.isoformat()
        dictionary["updated_at"] = self.updated_at.isoformat()
        if "_sa_instance_state" in dictionary.keys():
            del dictionary["_sa_instance_state"]
        return dictionary

    def delete(self):
        """deletes the current instance from the storage"""
        models.storage.delete(self)
