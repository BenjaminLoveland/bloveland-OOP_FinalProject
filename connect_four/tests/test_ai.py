"""
Module for Unittesting of ai.py
"""

import unittest
from unittest.mock import patch, MagicMock
from hypothesis import given, strategies as st

from ai import ConnectFourAI


class TestAI(unittest.TestCase):
    """
    Class to test the ai module.
    """

    @patch('ai.openai.ChatCompletion.create')
    def test_get_best_move_valid_response(self, mock_openai_create):
        """
        Test if get_best_move returns a valid column index on valid response.
        """
        # Mock API response
        mock_openai_create.return_value = MagicMock(
            choices=[MagicMock(message={'content': '4'})]
        )
        ai = ConnectFourAI(api_key="dummy_key")
        board = [[0] * 7 for _ in range(6)]
        result = ai.get_best_move(board)
        self.assertEqual(result, 3)  # Column 4 maps to index 3

    @patch('ai.openai.ChatCompletion.create')
    def test_get_best_move_invalid_response(self, mock_openai_create):
        """
        Test if get_best_move raises ValueError on invalid response.
        """
        # Mock invalid API response
        mock_openai_create.return_value = MagicMock(
            choices=[MagicMock(message={'content': 'invalid'})]
        )
        ai = ConnectFourAI(api_key="dummy_key")
        board = [[0] * 7 for _ in range(6)]
        with self.assertRaises(ValueError):
            ai.get_best_move(board)


if __name__ == "__main__":
    unittest.main()
