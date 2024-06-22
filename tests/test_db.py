import unittest
from unittest.mock import patch
import mongomock
from db_manager import *

class TestDBManager(unittest.TestCase):

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def setUp(self):
        self.client = db_connect()
        self.db = self.client[DB_NAME]
        self.collection_name = 'testcollection'
        self.collection = self.db[self.collection_name]
        self.collection.delete_many({})

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def tearDown(self):
        self.client.close()

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def test_add_user(self):
        result = add_user('testuser', 'testuser@example.com', 'password123')
        self.assertTrue(result)
        result = validate_user('testuser', 'password123')
        self.assertTrue(result)
        # result = add_user('testuser', 'anotheremail@example.com', 'password123')
        # self.assertEqual(result, 'Username testuser already exists!')

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def test_change_password(self):
        add_user('testuser', 'testuser@example.com', 'password123')
        result = change_password('testuser', 'newpassword123')
        self.assertTrue(result)
        result = validate_user('testuser', 'newpassword123')
        self.assertTrue(result)

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def test_change_email(self):
        add_user('testuser', 'testuser@example.com', 'password123')
        result = change_email('testuser', 'newemail@example.com')
        self.assertTrue(result)
        result = validate_user('newemail@example.com', 'password123')
        self.assertTrue(result)

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def test_validate_user(self):
        add_user('testuser', 'testuser@example.com', 'password123')
        result = validate_user('testuser', 'password123')
        self.assertTrue(result)
        result = validate_user('testuser@example.com', 'password123')
        self.assertTrue(result)
        # result = validate_user('testuser', 'wrongpassword')
        # self.assertEqual(result, 'Password is incorrect!')
        result = validate_user('nonexistentuser', 'password123')
        self.assertEqual(result, "User nonexistentuser doesn't exist!")

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def test_get_collection_with_documents(self):
        self.collection.insert_one({'key': 'value'})
        result = get_collection(self.collection_name)
        self.assertEqual(result['key'], 'value')

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def test_get_collection_empty(self):
        with self.assertRaises(IndexError) as context:
            get_collection(self.collection_name)
        self.assertTrue('list index out of range' in str(context.exception))

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def test_get_user_dict(self):
        add_user('testuser', 'testuser@example.com', 'password123')
        result = get_user_dict('testuser')
        self.assertEqual(result['username'], 'testuser')
        result = get_user_dict('testuser@example.com')
        self.assertEqual(result['email'], 'testuser@example.com')
        result = get_user_dict('nonexistentuser')
        self.assertEqual(result, "Found no such user")

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def test_update_user_start_riddle(self):
        add_user('testuser', 'testuser@example.com', 'password123')
        result = update_user_start_riddle('testuser', '123')
        self.assertFalse(result)

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def test_update_user_solved_riddle(self):
        add_user('testuser', 'testuser@example.com', 'password123')
        update_user_start_riddle('testuser', '123')
        result = update_user_solved_riddle('testuser', '123')
        self.assertTrue(result)
        result = update_user_solved_riddle('testuser', '456')
        self.assertFalse(result)

    @patch('db_manager.MongoClient', new=mongomock.MongoClient)
    def test_update_user_gaveup_riddle(self):
        add_user('testuser', 'testuser@example.com', 'password123')
        update_user_start_riddle('testuser', '123')
        result = update_user_gaveup_riddle('testuser', '123')
        self.assertTrue(result)
        result = update_user_gaveup_riddle('testuser', '456')
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
