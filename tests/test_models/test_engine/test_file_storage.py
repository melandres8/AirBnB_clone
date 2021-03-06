#!/usr/bin/python3
""" Unittest for FileStorage class module """
import os
import pep8
import unittest
from os import path
from models.city import City
from models.user import User
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """ FileStorage testing class
    """
    def test_docstring(self):
        """ Test docstring in module, class and function """
        self.assertTrue(len(FileStorage.__doc__) > 0)
        for funct in dir(FileStorage):
            self.assertTrue(len(funct.__doc__) > 0)

    def test_pep8(self):
        """ pep8 unittest
        """
        style = pep8.StyleGuide(quiet=True)
        file1_path = 'models/engine/file_storage.py'
        file2_path = 'tests/test_models/test_engine/test_file_storage.py'
        checking = style.check_files((file1_path, file2_path))
        mess = "Found code style errors (and warning)."
        self.assertEqual(checking.total_errors, 0, mess)

    def test_objects(self):
        """ Checking if objects exists
        """
        self.assertTrue(hasattr(FileStorage, '_FileStorage__objects'))

    def test_file_path(self):
        """ Checking the file path
        """
        path_file = FileStorage._FileStorage__file_path
        self.assertEqual(path_file, 'file.json')

    def test_isinstance(self):
        """ Checking if a new object is instace
            of FileStorage
        """
        new_ins = FileStorage()
        self.assertIsInstance(new_ins, FileStorage)

    def test_all(self):
        """ Checkig if all is returning a dict
        """
        fileStorage = FileStorage()
        new_obj = fileStorage.all()
        self.assertIsInstance(new_obj, dict)

    def test_new(self):
        """ Cheking when new object is created
        """
        fileStorage = FileStorage()
        new_obj = fileStorage.all()
        city = City()
        city.state_id = "123abc"
        city.name = "Cali"
        fileStorage.new(city)
        k = "{}.{}".format(type(city).__name__, city.id)
        self.assertIsNotNone(new_obj[k])

    def test_file_exist(self):
        """ Checking if JSON file exist
            and is reloading
        """
        user1 = User()
        fileStorage = FileStorage()
        k = "{}.{}".format(type(user1).__name__, user1.id)
        fileStorage.new(user1)
        fileStorage.save()
        self.assertTrue(path.exists('file.json'))

    def test_reload(self):
        """ Checking if the object reloads
            successfully
        """
        new_ins = BaseModel()
        fileStorage = FileStorage()
        FileStorage._FileStorage__objects = {}
        k = "{}.{}".format(type(new_ins).__name__, new_ins.id)
        fileStorage.new(new_ins)
        fileStorage.save()
        fileStorage.reload()
        self.assertIn(k, FileStorage._FileStorage__objects)

    def test_save_method(self):
        """ Checking if save method is saving
            correctly to read our file.
        """
        new_model = BaseModel()
        fileStorage = FileStorage()
        k = "{}.{}".format(type(new_model).__name__, new_model.id)
        fileStorage.new(new_model)
        fileStorage.save()
        with open('file.json', 'r') as file:
            self.assertIn(k, file.read())

    def test_permissions(self):
        """ Test for validate the permissions """
        read = os.access('models/engine/file_storage.py', os.R_OK)
        self.assertTrue(read)
        write = os.access('models/engine/file_storage.py', os.W_OK)
        self.assertTrue(write)
        exe = os.access('models/engine/file_storage.py', os.X_OK)
        self.assertTrue(exe)
