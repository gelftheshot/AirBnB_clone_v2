#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.city import City
import os
from unittest import skipIf
class test_City(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City
    @skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "Not supported in db") 
    def test_state_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.state_id), str)
    @skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db', "Not supported in db")
    def test_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)
