import unittest
from unittest.mock import patch
import mongomock
from db_manager import *

class TestDBManager(unittest.TestCase):

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def test_add_user(self):
        result = add_user('testuser', 'testuser@example.com', 'password123')
        self.assertTrue(result)
        result = validate_user('testuser', 'password123')
        self.assertTrue(result)
        result = add_user('testuser', 'anotheremail@example.com', 'password123')
        self.assertEqual(result, 'Username testuser already exists!')
        result = add_user('anotheruser', 'testuser@example.com', 'password123')
        self.assertEqual(result, 'Email testuser@example.com already exists!')

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def test_change_password(self):
        add_user('testuser', 'testuser@example.com', 'password123')
        result = change_password('testuser', 'newpassword123')
        self.assertTrue(result)
        result = validate_user('testuser', 'newpassword123')
        self.assertTrue(result)
        result = change_password('testuser@example.com', 'newpassword456')
        self.assertTrue(result)
        result = validate_user('testuser', 'newpassword456')
        self.assertTrue(result)

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def test_change_email(self):
        add_user('testuser', 'testuser@example.com', 'password123')
        result = change_email('testuser', 'newemail@example.com')
        self.assertTrue(result)
        result = validate_user('newemail@example.com', 'password123')
        self.assertTrue(result)

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def test_update_solved_riddle(self):
        add_user('testuser', 'testuser@example.com', 'password123')
        result = update_solved_riddle('testuser', 'riddle1', 120)
        # missing get solved riddle for user
        self.assertIsNone(result)

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def test_validate_user(self):
        add_user('testuser', 'testuser@example.com', 'password123')
        result = validate_user('testuser', 'password123')
        self.assertTrue(result)
        result = validate_user('testuser@example.com', 'password123')
        self.assertTrue(result)
        result = validate_user('testuser', 'wrongpassword')
        self.assertEqual(result, 'Password is incorrect!')
        result = validate_user('nonexistentuser', 'password123')
        self.assertEqual(result, "User nonexistentuser doesn't exist!")

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def test_get_collection(self):
        client = db_connect()
        db = client['guessquest']
        collection = db['testcollection']
        collection.insert_one({'key': 'value'})

        result = get_collection('testcollection')
        self.assertEqual(result['key'], 'value')

if __name__ == '__main__':
    unittest.main()
