import unittest
from unittest.mock import patch
from riddle_generator import *

class TestRiddleGenerator(unittest.TestCase):

    def test_generate_random_number(self):
        number = generate_random_number()
        self.assertEqual(len(number), 4)
        self.assertTrue(all(number.count(digit) <= 2 for digit in number))

    def test_choose_digit_and_index(self):
        number = "1234"
        digit, index = choose_digit_and_index(number)
        self.assertIn(digit, number)
        self.assertIn(index, range(4))
        self.assertEqual(digit, number[index])

    @patch('riddle_generator.generate_random_number')
    def test_generate_new_number_with_same_digit(self, mock_generate_random_number):
        mock_generate_random_number.return_value = "5678"
        digit, index = '5', 0
        new_number = generate_new_number_with_same_digit(digit, index)
        self.assertEqual(new_number[index], digit)
        self.assertNotEqual(new_number, "5678")

    def test_choose_two_digits_and_indices(self):
        number = "1234"
        digits, indices = choose_two_digits_and_indices(number)
        self.assertEqual(len(digits), 2)
        self.assertEqual(len(indices), 2)
        self.assertNotEqual(indices[0], indices[1])
        self.assertIn(digits[0], number)
        self.assertIn(digits[1], number)
        self.assertEqual(digits[0], number[indices[0]])
        self.assertEqual(digits[1], number[indices[1]])

    @patch('riddle_generator.generate_random_number')
    def test_generate_new_number_with_two_digits(self, mock_generate_random_number):
        mock_generate_random_number.return_value = "5678"
        digits = ['5', '6']
        indices = [0, 1]
        original_digits = set("1234")
        new_number = generate_new_number_with_two_digits(digits, indices, original_digits)
        self.assertNotEqual(new_number, "5678")
        self.assertIn(digits[0], new_number)
        self.assertIn(digits[1], new_number)

    @patch('riddle_generator.generate_random_number')
    def test_generate_new_number_with_two_digits_at_same_indices(self, mock_generate_random_number):
        mock_generate_random_number.return_value = "5678"
        digits = ['5', '6']
        indices = [0, 1]
        original_digits = set("1234")
        new_number = generate_new_number_with_two_digits_at_same_indices(digits, indices, original_digits)
        self.assertNotEqual(new_number, "5678")
        self.assertEqual(new_number[indices[0]], digits[0])
        self.assertEqual(new_number[indices[1]], digits[1])

    def test_generate_unique_number(self):
        original_number = "1234"
        unique_number = generate_unique_number(original_number)
        self.assertEqual(len(unique_number), 4)
        self.assertTrue(all(digit not in original_number for digit in unique_number))

    def test_is_valid_number(self):
        hint1 = "1234"
        hint2 = "2143"
        hint3 = "1256"
        hint4 = "7890"
        self.assertTrue(is_valid_number("1234", hint1, hint2, hint3, hint4))
        self.assertFalse(is_valid_number("5678", hint1, hint2, hint3, hint4))

if __name__ == '__main__':
    unittest.main()
