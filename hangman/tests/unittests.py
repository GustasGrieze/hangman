import unittest
from hangman.models import generate_game_id, choose_random_word


class TestFunctionTypes(unittest.TestCase):
    def test_game_id(self) -> None:
        self.assertEqual(int, type(generate_game_id()))
    
    def test_is_word_string(self) -> None:
        self.assertEqual(str, type(choose_random_word()))
    

class TestGenerateGameId(unittest.TestCase):
    def test_generate_game_id(self) -> None:

        game_id = generate_game_id()
        self.assertGreaterEqual(game_id, 1e9)
        self.assertLess(game_id, 1e10)

        game_id1 = generate_game_id()
        game_id2 = generate_game_id()
        self.assertNotEqual(game_id1, game_id2)


class TestChooseRandomWord(unittest.TestCase):
    def test_choose_random_word(self) -> None:

        random_word = choose_random_word()
        self.assertTrue(len(random_word) > 0)

        self.assertTrue(random_word.isalpha())
        self.assertTrue(random_word.isupper())


if __name__ == '__main__':
    unittest.main()