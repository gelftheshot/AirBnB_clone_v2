#!/usr/bin/python3
import unittest
import os
import models
from unittest.mock import patch
from io import StringIO
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from models.engine.db_storage import DBStorage
import random
import string


class TestHBNBCommand(unittest.TestCase):
    """
    
    """

    @classmethod

    def setUpClass(cls):
        """
        
        """
        try:
            os.rename("file.json", "test_file.json")
        except IOError:
            pass
        cls.HBNB = HBNBCommand()

    @classmethod

    def tearDownClass(cls):
        """
        """
        try:
            os.rename("test_file.json", "file.json")
        except IOError:
            pass
        del cls.HBNB

    def setUp(self) -> None:
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_create(self):
        """"""
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("create BaseModel")
            base_m = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("all BaseModel")
            self.assertIn(base_m, output.getvalue())
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("create User")
            user = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("all User")
            self.assertIn(user, output.getvalue())
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("create State")
            state = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("all State")
            self.assertIn(state, output.getvalue())
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("create City")
            city = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("all City")
            self.assertIn(city, output.getvalue())
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("create Amenity")
            amenity = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("all Amenity")
            self.assertIn(amenity, output.getvalue())
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("create Place")
            place = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("all Place")
            self.assertIn(place, output.getvalue())
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("create Review")
            review = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("all Review")
            self.assertIn(review, output.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_create_with_kwargs(self):
        """"
        """
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("create User email=\"example@gmailcom\" password=\"1234\" first_name=\"gelfeto\" last_name=\"gebre\"")
            user = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("all User")
            output = output.getvalue().strip()
            self.assertIn(user, output)
            self.assertIn("'email': 'example@gmailcom'", output)
            self.assertIn("'password': '1234'", output)
            self.assertIn("'first_name': 'gelfeto'", output)
            self.assertIn("'last_name': 'gebre'", output)
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("create State name=\"Amhara\"")
            state = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("all State")
            output = output.getvalue().strip()
            self.assertIn(state, output)
            self.assertIn("'name': 'Amhara'", output)
        with patch("sys.stdout", new=StringIO()) as output: 
            self.HBNB.onecmd("create City state_id=\"1234\" name=\"Gonder\"")
            city = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("all City")
            output = output.getvalue().strip()
            self.assertIn(city, output)
            self.assertIn("'state_id': '1234'", output)
            self.assertIn("'name': 'Gonder'", output)
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("create Amenity name=\"Wifi\"")
            amenity = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("all Amenity")
            output = output.getvalue().strip()
            self.assertIn(amenity, output)
            self.assertIn("'name': 'Wifi'", output)
        def generate_random_string(length):
            letters = string.ascii_letters
            return ''.join(random.choice(letters) for i in range(length))

        def generate_random_number():
            return random.randint(1, 100)

        with patch("sys.stdout", new=StringIO()) as output:
            user_id = generate_random_string(6)
            name = generate_random_string(10)
            number_rooms = generate_random_number()
            number_bathrooms = generate_random_number()
            max_guest = generate_random_number()
            price_by_night = generate_random_number()
            latitude = random.uniform(-90, 90)
            longitude = random.uniform(-180, 180)

            self.HBNB.onecmd(f"create Place city_id=\"1234\" user_id=\"{user_id}\" name=\"{name}\" number_rooms=\"{number_rooms}\" number_bathrooms=\"{number_bathrooms}\" max_guest=\"{max_guest}\" price_by_night=\"{price_by_night}\" latitude=\"{latitude}\" longitude=\"{longitude}\"")
            place = output.getvalue().strip()

        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("all Place")
            output = output.getvalue().strip()
            self.assertIn(place, output)
            self.assertIn(f"'city_id': '1234'", output)
            self.assertIn(f"'user_id': '{user_id}'", output)
            self.assertIn(f"'name': '{name}'", output)
            self.assertIn(f"'number_rooms': '{number_rooms}'", output)
            self.assertIn(f"'number_bathrooms': '{number_bathrooms}'", output)
            self.assertIn(f"'max_guest': '{max_guest}'", output)
            self.assertIn(f"'price_by_night': '{price_by_night}'", output)
            self.assertIn(f"'latitude': '{latitude}'", output)
            self.assertIn(f"'longitude': '{longitude}'", output)

        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("create Review place_id=\"1234\" user_id=\"1234\" text=\"what_a_place\"")
            review = output.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as output:
            self.HBNB.onecmd("all Review")
            output = output.getvalue().strip()
            self.assertIn(review, output)
            self.assertIn("'place_id': '1234'", output)
            self.assertIn("'user_id': '1234'", output)
            self.assertIn("'text': 'what a place'", output)