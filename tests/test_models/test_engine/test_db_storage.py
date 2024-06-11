#!/usr/bin/python3
"""document document"""

from models.engine import db_storage
from datetime import datetime
import inspect
import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import unittest
from models import storage



DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_type != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
    
    def test_get(self):
        """Test the get method"""
        # Test with an existing ID
        state = storage.get(State, self.state.id)
        self.assertEqual(state.id, self.state.id)

        # Test with a non-existing ID
        state = storage.get(State, "non-existing-id")
        self.assertIsNone(state)

    def test_count(self):
        """Test the count method"""
        # Test with a class
        count = storage.count(State)
        self.assertEqual(count, 1)

        # Test without a class
        count = storage.count()
        self.assertGreaterEqual(count, 1)
