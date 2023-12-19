#!/usr/bin/python3
"""This module defines mysql storage engine"""
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from sqlalchemy import create_engine


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """Initializes a new instance of the DBStorage class."""
        mysql_user = getenv("HBNB_MYSQL_USER")
        mysql_pwd = getenv("HBNB_MYSQL_PWD")
        mysql_host = getenv("HBNB_MYSQL_HOST")
        mysql_db = getenv("HBNB_MYSQL_DB")
        hbnb_env = getenv("HBNB_ENV")
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                mysql_user, mysql_pwd, mysql_host, mysql_db
            ),
            pool_pre_ping=True,
        )

        if hbnb_env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        classes = {
            "User": User,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Place": Place,
            "Review": Review,
        }

        new_dict = {}
        if cls is None:
            for key, value in classes.items():
                for obj in self.__session.query(value):
                    key = obj.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj
        else:
            for obj in self.__session.query(classes[cls]):
                key = obj.__class__.__name__ + "." + obj.id
                new_dict[key] = obj

        return new_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        from sqlalchemy.orm import sessionmaker, scoped_session

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()
