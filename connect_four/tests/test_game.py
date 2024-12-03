"""
Module for Unittesting of game.py
"""

import unittest
from hypothesis import given, strategies as st  # type: ignore

from game import Game


class TestGame(unittest.TestCase):
    """
    Class to test the game module.
    """

    def setUp(self):
        """
        Initialize a new Game instance before each test.
        """
        self.game = Game()

    def test_reset_board(self):
        """
        Test that reset_board correctly initializes the board.
        """
        self.game.board = [[1] * 7 for _ in range(6)]
        self.game.reset_board()
        expected_board = [[0] * 7 for _ in range(6)]
        self.assertEqual(self.game.board, expected_board)

    @given(st.integers(min_value=0, max_value=6))
    def test_make_move_valid_column(self, column):
        """
        Test making a move in a valid column and verify board state.
        """
        # Get the current player before making the move
        current_player = self.game.current_player
        row, _ = self.game.make_move(column)
        # Assert the move was made correctly
        self.assertEqual(self.game.board[row][column], current_player)

    @given(st.integers(min_value=0, max_value=6))
    def test_make_move_full_column(self, column):
        """
        Test that making a move in a full column raises ValueError.
        """
        for _ in range(self.game.rows):
            self.game.make_move(column)

        with self.assertRaises(ValueError):
            self.game.make_move(column)

    def test_check_winner_horizontal(self):
        """
        Test for horizontal winner detection.
        """
        self.game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0],
        ]
        self.assertEqual(self.game.check_winner(), 1)

    def test_check_winner_vertical(self):
        """
        Test for vertical winner detection.
        """
        self.game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
        ]
        self.assertEqual(self.game.check_winner(), 1)

    def test_check_winner_diagonal(self):
        """
        Test for diagonal winner detection.
        """
        self.game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
        ]
        self.assertEqual(self.game.check_winner(), 1)

    def test_check_winner_diagonal_backward(self):
        """
        Test for diagonal winner detection with backward slope (/).
        """
        self.game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
        ]
        self.assertEqual(self.game.check_winner(), 1)

    def test_make_move_full_column_error(self):
        """
        Test making move in full collumn raises a ValueError.
        """
        for _ in range(self.game.rows):
            self.game.make_move(0)

        with self.assertRaises(ValueError):
            self.game.make_move(0)

    @given(st.lists(st.lists(st.integers(min_value=0, max_value=2), min_size=7,
                    max_size=7), min_size=6, max_size=6))
    def test_board_dimensions(self, board):
        """
        Test setting the board with valid and invalid dimensions.
        """
        try:
            self.game.board = board
            self.assertEqual(self.game.board, board)
        except ValueError:
            self.assertNotEqual(
                len(board), 6) or self.assertNotEqual(len(board[0]), 7)

    def test_is_column_full(self):
        """
        Test is_column_full method for full and non-full columns.
        """
        self.game.board = [[1] * 7 for _ in range(6)]
        for col in range(self.game.columns):
            self.assertTrue(self.game.is_column_full(col))

        self.game.board = [[0] * 7 for _ in range(6)]
        for col in range(self.game.columns):
            self.assertFalse(self.game.is_column_full(col))

    def test_board_setter_invalid_dimensions(self):
        """
        Test that setting the board with wrong dimensions raises ValueError.
        """
        with self.assertRaises(ValueError):
            self.game.board = [[1] * 8 for _ in range(6)]  # Too many columns
        with self.assertRaises(ValueError):
            self.game.board = [[1] * 7 for _ in range(5)]  # Too few rows

    def test_make_move_out_of_bounds(self):
        """
        Test that making a move out of bounds raises ValueError.
        """
        with self.assertRaises(ValueError):
            self.game.make_move(-1)  # Column index too low
        with self.assertRaises(ValueError):
            self.game.make_move(7)  # Column index too high

    def test_to_string(self):
        """
        Test the string representation of the board.
        """
        expected_output = "\n".join(["0 0 0 0 0 0 0" for _ in range(6)])
        self.assertEqual(self.game.to_string(), expected_output)

    def test_invalid_player_number(self):
        """
        Test setting an invalid player number raises ValueError.
        """
        with self.assertRaises(ValueError):
            self.game.current_player = 3

        with self.assertRaises(ValueError):
            self.game.current_player = 0

    def test_current_player_setter_valid(self):
        """
        Test that setting updates the player number.
        """
        self.game.current_player = 1
        self.assertEqual(self.game.current_player, 1)

        self.game.current_player = 2
        self.assertEqual(self.game.current_player, 2)

    def test_check_winner_no_winner(self):
        """
        Test that check_winner returns 0 when there is no winner.
        """
        self.game.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
        self.assertEqual(self.game.check_winner(), 0)


if __name__ == "__main__":
    unittest.main()
