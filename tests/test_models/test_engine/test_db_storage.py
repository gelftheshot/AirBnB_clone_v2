#!/usr/bin/python3
import unittest
import os
import MySQLdb
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.base_model import Base
from models.engine.db_storage import DBStorage
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.engine.base import Engine
from models.engine.db_storage import DBStorage


class TestDBStorage(unittest.TestCase):
    """
    """

    @classmethod
    def setUpClass(cls):
        """DBStorage testing setup.
        """
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            cls.storage = DBStorage()
            Base.metadata.create_all(cls.storage._DBStorage__engine)
            Session = sessionmaker(bind=cls.storage._DBStorage__engine)
            cls.storage._DBStorage__session = Session()
            cls.state = State(name="Texas")
            cls.storage._DBStorage__session.add(cls.state)
            cls.city = City(name="Dalas", state_id=cls.state.id)
            cls.storage._DBStorage__session.add(cls.city)
            cls.user = User(email="example@gmail.com", password="password")
            cls.storage._DBStorage__session.add(cls.user)
            cls.place = Place(city_id=cls.city.id, user_id=cls.user.id,
                                name="Hotel")
            cls.storage._DBStorage__session.add(cls.place)
            cls.amenity = Amenity(name="Wifi")
            cls.storage._DBStorage__session.add(cls.amenity)
            cls.review = Review(place_id=cls.place.id, user_id=cls.user.id,
                                text="Great_place_to_stay")
            cls.storage._DBStorage__session.add(cls.review)
            cls.storage._DBStorage__session.commit()
    @classmethod
    def tearDownClass(cls):
        """DBStorage testing teardown.
        """
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            cls.storage._DBStorage__session.delete(cls.state)
            cls.storage._DBStorage__session.delete(cls.city)
            cls.storage._DBStorage__session.delete(cls.user)
            cls.storage._DBStorage__session.delete(cls.amenity)
            cls.storage._DBStorage__session.commit()
            del cls.state
            del cls.city
            del cls.user
            del cls.place
            del cls.amenity
            del cls.review
            cls.storage._DBStorage__session.close()
            del cls.storage

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 
                     "Testing FileStorage")
    def test_if_methods_exist(self):
        """Test if class attributes exist.
        """
        self.assertTrue(hasattr(DBStorage, '__init__'))
        self.assertTrue(hasattr(DBStorage, 'all'))
        self.assertTrue(hasattr(DBStorage, 'new'))
        self.assertTrue(hasattr(DBStorage, 'save'))
        self.assertTrue(hasattr(DBStorage, 'delete'))
        self.assertTrue(hasattr(DBStorage, 'reload'))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "Testing FileStorage")
    def test_init(self):
        """Test instantiation of DBStorage class.
        """
        self.assertTrue(isinstance(self.storage, DBStorage))
        self.assertTrue(isinstance(self.storage._DBStorage__engine, Engine))
        self.assertTrue(isinstance(self.storage._DBStorage__session, Session))
        self.assertTrue(self.storage._DBStorage__engine is not None)
        self.assertTrue(self.storage._DBStorage__session is not None)
    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "Testing FileStorage")
    def test_all(self):
        """
        testing db all method
        """
        new = self.storage.all()
        self.assertIsInstance(new, dict)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "Testing FileStorage")
    def test_new(self):
        """Test new method."""
        st = State(name="Washington")
        self.storage.new(st)
        store = list(self.storage._DBStorage__session.new)
        self.assertIn(st, store)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "Testing FileStorage")
    def test_save_one_create(self):
        st = State(name="New_mexico")
        self.storage._DBStorage__session.add(st)
        self.storage.save()
        db = MySQLdb.connect(user="hbnb_test",
                             passwd="hbnb_test_pwd",
                             db="hbnb_test_db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM states WHERE BINARY name = 'New_mexico'")
        query = cursor.fetchall()
        self.assertEqual(1, len(query))
        cursor.close()


    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "Testing FileStorage")
    def test_delete(self):
        """Test delete method."""
        new_york = State(name="New_York")
        self.storage._DBStorage__session.add(new_york)
        self.storage._DBStorage__session.commit()
        self.storage.delete(new_york)
        self.assertIn(new_york, list(self.storage._DBStorage__session.deleted))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 
                     "Testing FileStorage")
    def test_reload(self):
        """Test reload method."""
        current_ses = self.storage._DBStorage__session
        self.storage.reload()
        self.assertNotEqual(current_ses, self.storage._DBStorage__session)
        self.storage._DBStorage__session.close()
        self.storage._DBStorage__session = current_ses


if __name__ == "__main__":
    unittest.main()