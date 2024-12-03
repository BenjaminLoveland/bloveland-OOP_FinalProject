import unittest
from unittest.mock import patch
from flask import Flask, jsonify
from app import app
from game import Game
from ai import ConnectFourAI


class TestApp(unittest.TestCase):
    """
    Class to test the app module.
    """

    def setUp(self):
        """
        Sets up the Flask test client.
        """
        self.app = app.test_client()
        self.app.testing = True

    @patch.object(Game, 'reset_board')
    def test_start_game(self, mock_reset_board):
        """
        Tests the '/start-game' route.
        """
        mock_reset_board.return_value = None
        response = self.app.post('/start-game')

        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['message'], 'New game started!')

    @patch.object(Game, 'reset_board')
    def test_start_game_error(self, mock_reset_board):
        """
        Tests the '/start-game' route when an exception is raised.
        """
        mock_reset_board.side_effect = Exception("Test exception")
        response = self.app.post('/start-game')

        self.assertEqual(response.status_code, 500)
        json_data = response.get_json()
        self.assertEqual(json_data['error'], "Test exception")

    @patch.object(ConnectFourAI, 'get_best_move')
    @patch.object(Game, 'is_column_full')
    @patch.object(Game, 'make_move')
    @patch.object(Game, 'check_winner')
    def test_get_move(
        self, mock_check_winner, mock_make_move,
            mock_is_column_full, mock_get_best_move):
        """
        Tests the '/get-move' route.
        """
        mock_get_best_move.return_value = 3
        mock_is_column_full.return_value = False
        mock_make_move.return_value = None
        mock_check_winner.return_value = 0

        board = [[0] * 7 for _ in range(6)]
        data = {"board": board}

        response = self.app.post('/get-move', json=data)
        self.assertEqual(response.status_code, 200)

        json_data = response.get_json()
        self.assertEqual(json_data['move'], 4)

    def test_get_move_invalid_data(self):
        """
        Tests the '/get-move' route with invalid board data (missing "board").
        """
        data = {}  # Missing 'board' key
        response = self.app.post('/get-move', json=data)

        self.assertEqual(response.status_code, 400)
        json_data = response.get_json()
        self.assertEqual(json_data['error'], "Invalid board data")

    @patch.object(ConnectFourAI, 'get_best_move')
    @patch.object(Game, 'is_column_full')
    def test_get_move_column_full(
            self, mock_is_column_full, mock_get_best_move):
        """
        Tests the '/get-move' route when AI suggests a full column.
        """
        mock_get_best_move.return_value = 3
        mock_is_column_full.return_value = True

        board = [[0] * 7 for _ in range(6)]
        data = {"board": board}

        response = self.app.post('/get-move', json=data)

        self.assertEqual(response.status_code, 500)
        json_data = response.get_json()
        self.assertEqual(json_data['error'], "AI suggested a full column")

    @patch.object(Game, 'check_winner')
    def test_check_winner(self, mock_check_winner):
        """
        Tests the '/check-winner' route.
        """
        mock_check_winner.return_value = 1
        board = [[0] * 7 for _ in range(6)]
        board[5][0] = 1
        data = {"board": board}

        response = self.app.post('/check-winner', json=data)
        self.assertEqual(response.status_code, 200)

        json_data = response.get_json()
        self.assertEqual(json_data['winner'], 1)

    def test_check_winner_invalid_data(self):
        """
        Tests the '/check-winner' route with invalid board data.
        """
        data = {}
        response = self.app.post('/check-winner', json=data)

        self.assertEqual(response.status_code, 400)
        json_data = response.get_json()
        self.assertEqual(json_data['error'], "Invalid board data")

    @patch.object(Game, 'check_winner')
    def test_check_winner_with_fixed_board(self, mock_check_winner):
        """
        Tests the '/check-winner' route with a manually created board.
        """
        mock_check_winner.return_value = 1
        board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0],
        ]
        data = {"board": board}

        response = self.app.post('/check-winner', json=data)
        self.assertEqual(response.status_code, 200)

        json_data = response.get_json()
        self.assertEqual(json_data['winner'], 1)


if __name__ == '__main__':
    unittest.main()
