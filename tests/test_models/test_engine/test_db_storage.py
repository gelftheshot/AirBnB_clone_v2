#!/usr/bin/python3
import unittest
import MySQLdb
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
import pep8
from models.review import Review
from models.engine.file_storage import FileStorage
from models.place import Place
from models.base_model import Base
from models.engine.db_storage import DBStorage
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.engine.base import Engine
from models.engine.db_storage import DBStorage


class TestDatabaseStorage(unittest.TestCase):
    """Unittests for testing the DatabaseStorage class."""

    @classmethod
    def setUpClass(cls):
        """DatabaseStorage testing setup.

        Creates instances of all class types for testing.
        """
        if type(models.storage) == DBStorage:
            cls.storage = DBStorage()
            Base.metadata.create_all(cls.storage._DBStorage__engine)
            Session = sessionmaker(bind=cls.storage._DBStorage__engine)
            cls.storage._DBStorage__session = Session()
            cls.state_obj = State(name="California")
            cls.storage._DBStorage__session.add(cls.state_obj)
            cls.city_obj = City(name="Los Angeles", state_id=cls.state_obj.id)
            cls.storage._DBStorage__session.add(cls.city_obj)
            cls.user_obj = User(email="test@gmail.com", password="test")
            cls.storage._DBStorage__session.add(cls.user_obj)
            cls.place_obj = Place(city_id=cls.city_obj.id, user_id=cls.user_obj.id,
                                name="Test Hotel")
            cls.storage._DBStorage__session.add(cls.place_obj)
            cls.amenity_obj = Amenity(name="Pool")
            cls.storage._DBStorage__session.add(cls.amenity_obj)
            cls.review_obj = Review(place_id=cls.place_obj.id, user_id=cls.user_obj.id,
                                text="Amazing place to stay")
            cls.storage._DBStorage__session.add(cls.review_obj)
            cls.storage._DBStorage__session.commit()

    @classmethod
    def tearDownClass(cls):
        """DatabaseStorage testing teardown.

        Delete all test class instances.
        """
        if type(models.storage) == DBStorage:
            cls.storage._DBStorage__session.delete(cls.state_obj)
            cls.storage._DBStorage__session.delete(cls.city_obj)
            cls.storage._DBStorage__session.delete(cls.user_obj)
            cls.storage._DBStorage__session.delete(cls.amenity_obj)
            cls.storage._DBStorage__session.commit()
            del cls.state_obj
            del cls.city_obj
            del cls.user_obj
            del cls.place_obj
            del cls.amenity_obj
            del cls.review_obj
            cls.storage._DBStorage__session.close()
            del cls.storage

    @unittest.skipIf(type(models.storage) == FileStorage,
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

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")    
    def test_init(self):
        """Test instantiation of DBStorage class.
        """
        self.assertTrue(isinstance(self.storage, DBStorage))
        self.assertTrue(isinstance(self.storage._DBStorage__engine, Engine))
        self.assertTrue(isinstance(self.storage._DBStorage__session, Session))
        self.assertTrue(self.storage._DBStorage__engine is not None)
        self.assertTrue(self.storage._DBStorage__session is not None)
    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")    
    def test_all(self):
        """
        testing db all method
        """
        new = self.storage.all()
        self.assertIsInstance(new, dict)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_new(self):
        """
        testing db new method
        """
        new = self.storage.all()
        obj = State(name="California")
        self.storage.new(obj)
        self.storage.save()
        key = obj.__class__.__name__ + "." + obj.id
        self.assertIsNotNone(new[key])
        lis = list(self.storage._DBStorage__session.new)
        self.assertIn(obj, list)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
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
        self.assertEqual(st.id, query[0][0])
        cursor.close()

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_save_two_create(self):
        """
        testing db save method
        """
        db = MySQLdb.connect(user="hbnb_test",
                             passwd="hbnb_test_pwd",
                             db="hbnb_test_db",
                             host="localhost")
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM states WHERE BINARY name = 'Virginia'")
        count_1 = cursor.fetchone()[0]

        st = State(name="Virginia")
        self.storage._DBStorage__session.add(st)
        self.storage.save()

        cursor.execute("SELECT COUNT(*) FROM states WHERE BINARY name = 'Virginia'")
        count_2 = cursor.fetchone()[0]

        self.assertEqual(count_1 + 1, count_2)

        cursor.close()
    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_delete(self):
        """Test delete method."""
        new_york = State(name="New_York")
        self.storage._DBStorage__session.add(new_york)
        self.storage._DBStorage__session.commit()
        self.storage.delete(new_york)
        self.assertIn(new_york, list(self.storage._DBStorage__session.deleted))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    @unittest.skipIf(type(models.storage) == FileStorage,
                     "This test is skipped for FileStorage")
    def test_reload(self):
        """Test the reload method of the DBStorage class.

        This test checks if the reload method correctly creates a new
        SQLAlchemy session. It does this by comparing the session before
        and after calling reload.
        """
        current_ses = self.storage._DBStorage__session
        self.storage.reload()
        self.assertNotEqual(current_ses, self.storage._DBStorage__session)
        self.storage._DBStorage__session.close()
        self.storage._DBStorage__session = current_ses

    def test_pep8(self):
        """Test if the code in db_storage.py follows PEP8 style guide.

        This test uses the pep8 module to check if the code in the
        db_storage.py file follows the PEP8 style guide. It asserts that
        the total number of PEP8 errors in the file is 0.
        """
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")
    
    def test_docstrings_for_all_methods(self):
        """Test if all methods in the DBStorage class have docstrings.

        This test checks if the class itself and all its methods have
        docstrings. It asserts that the docstring of each method is not
        None.
        """
        self.assertIsNotNone(DBStorage.__doc__)
        self.assertIsNotNone(DBStorage.__init__.__doc__)
        self.assertIsNotNone(DBStorage.all.__doc__)
        self.assertIsNotNone(DBStorage.new.__doc__)
        self.assertIsNotNone(DBStorage.save.__doc__)
        self.assertIsNotNone(DBStorage.delete.__doc__)
        self.assertIsNotNone(DBStorage.reload.__doc__)

if __name__ == "__main__":
    unittest.main()