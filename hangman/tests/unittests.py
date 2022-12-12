import unittest
from hangman.models import generate_game_id, choose_random_word


class TestFunctionTypes(unittest.TestCase):
    def test_game_id(self) -> None:
        self.assertEqual(int, type(generate_game_id()))
    
    def test_is_word_string(self) -> None:
        self.assertEqual(str, type(choose_random_word()))
    

if __name__ == '__main__':
    unittest.main()