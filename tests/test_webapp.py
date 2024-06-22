import unittest
from unittest.mock import patch
from webapp import *

class TestWebApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Guess Quest!', response.data)

    @patch('db_manager.validate_user')
    def test_login(self, mock_validate_user):
        mock_validate_user.return_value = True
        response = self.app.post('/login', data=dict(username='testuser', password='password123'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        mock_validate_user.return_value = "Invalid credentials"
        response = self.app.post('/login', data=dict(username='testuser', password='wrongpassword'))
        self.assertEqual(response.status_code, 200)

    @patch('db_manager.add_user')
    def test_signup(self, mock_add_user):
        mock_add_user.return_value = True
        response = self.app.post('/signup', data=dict(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            confirm_password='password123'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @patch('db_manager.get_collection')
    def test_riddle(self, mock_get_collection):
        mock_get_collection.return_value = {
            'hints': ['1234', '5678', '9101', '1213']
        }
        response = self.app.get('/riddle')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'1234', response.data)
        self.assertIn(b'5678', response.data)
        self.assertIn(b'9101', response.data)
        self.assertIn(b'1213', response.data)

    @patch('riddle_generator.is_valid_number')
    def test_check_user_answer(self, mock_is_valid_number):
        mock_is_valid_number.return_value = True
        response = self.app.post('/check_user_answer', data=dict(answer='1234'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'true', response.data)

        mock_is_valid_number.return_value = False
        response = self.app.post('/check_user_answer', data=dict(answer='5678'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'false', response.data)

    @patch('riddle_generator.get_scores')
    def test_riddle_scoreboard(self, mock_get_scores):
        mock_get_scores.return_value = [
            {'name': 'user1', 'timeInSeconds': 30},
            {'name': 'user2', 'timeInSeconds': 45}
        ]
        response = self.app.get('/finished')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'user1', response.data)
        self.assertIn(b'user2', response.data)
        self.assertIn(b'30', response.data)
        self.assertIn(b'45', response.data)

    @patch('riddle_generator.get_losers')
    @patch('riddle_generator.get_number_of_riddle_solutions')
    def test_riddle_losers_board(self, mock_get_losers, mock_get_number_of_riddle_solutions):
        mock_get_losers.return_value = [
            {'name': 'user1', 'timeInSeconds': 120},
            {'name': 'user2', 'timeInSeconds': 150}
        ]
        mock_get_number_of_riddle_solutions.return_value = 4
        response = self.app.get('/gave_up')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'user1', response.data)
        self.assertIn(b'user2', response.data)
        self.assertIn(b'120', response.data)
        self.assertIn(b'150', response.data)

if __name__ == '__main__':
    unittest.main()
