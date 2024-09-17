# Пишем тесты для классов
import unittest
from unittest.mock import patch
from loto_game import Card, Barrel, Player, HumanPlayer, ComputerPlayer, Game

class TestCard(unittest.TestCase):
    def setUp(self):
        self.card = Card()

    def test_card_initialization(self):
        self.assertEqual(len(self.card.card), 3)
        self.assertEqual(len(self.card.card[0]), 9)

    def test_card_numbers_count(self):
        numbers_count = sum(1 for row in self.card.card for num in row if isinstance(num, int))
        self.assertEqual(numbers_count, 15)

    def test_mark_number(self):
        # Находим число на карточке
        number_to_mark = next(num for row in self.card.card for num in row if isinstance(num, int))
        self.assertTrue(self.card.mark_number(number_to_mark))
        
        # Проверяем, что число отмечено
        self.assertIn('X', [item for row in self.card.card for item in row])

    def test_is_complete(self):
        self.assertFalse(self.card.is_complete())
        
        # Отмечаем все числа
        for row in self.card.card:
            for i in range(len(row)):
                if isinstance(row[i], int):
                    row[i] = 'X'
        
        self.assertTrue(self.card.is_complete())

class TestBarrel(unittest.TestCase):
    def test_barrel_initialization(self):
        barrel = Barrel(42)
        self.assertEqual(barrel.number, 42)

    def test_barrel_str_representation(self):
        barrel = Barrel(7)
        self.assertEqual(str(barrel), "7")

    def test_barrel_range(self):
        with self.assertRaises(ValueError):
            Barrel(0)
        with self.assertRaises(ValueError):
            Barrel(91)
        Barrel(1)
        Barrel(90)

class TestPlayer(unittest.TestCase):
    def test_player_initialization(self):
        player = Player("Test Player", 2)
        self.assertEqual(player.name, "Test Player")
        self.assertEqual(len(player.cards), 2)

class TestHumanPlayer(unittest.TestCase):
    def setUp(self):
        self.human_player = HumanPlayer("Human", 1)

    def test_human_player_initialization(self):
        self.assertEqual(self.human_player.name, "Human")
        self.assertEqual(len(self.human_player.cards), 1)

class TestComputerPlayer(unittest.TestCase):
    def setUp(self):
        self.computer_player = ComputerPlayer("Computer", 1)

    def test_computer_player_initialization(self):
        self.assertEqual(self.computer_player.name, "Computer")
        self.assertEqual(len(self.computer_player.cards), 1)

    def test_computer_player_make_move(self):
        barrel = Barrel(42)
        self.assertTrue(self.computer_player.make_move(barrel))

class TestGame(unittest.TestCase):
    @patch('builtins.input', side_effect=['1', '2', '10'])
    def test_game_initialization(self, mock_input):
        game = Game()
        self.assertEqual(len(game.players), 2)
        self.assertEqual(game.players[0].name, "Игрок 1")
        self.assertEqual(game.players[1].name, "Компьютер")
        self.assertEqual(len(game.barrels), 90)
        self.assertEqual(game.time_limit, 10)

    @patch('builtins.input', side_effect=['1', '2', '10'])
    def test_game_next_turn(self, mock_input):
        game = Game()
        with patch.object(game.players[0], 'make_move', return_value=True):
            with patch.object(game.players[1], 'make_move', return_value=True):
                self.assertFalse(game.next_turn())

    @patch('builtins.input', side_effect=['1', '2', '10'])
    def test_game_check_winner(self, mock_input):
        game = Game()
        self.assertFalse(game.check_winner())
        for card in game.players[0].cards:
            for row in card.card:
                for i in range(len(row)):
                    if isinstance(row[i], int):
                        row[i] = 'X'
        self.assertTrue(game.check_winner())

if __name__ == '__main__':
    unittest.main()
