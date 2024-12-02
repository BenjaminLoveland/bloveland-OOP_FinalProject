"""
AI module to handle interactions with chatGPT
"""

import openai


class ConnectFourAI:
    def __init__(self, api_key):
        openai.api_key = (
            
        )

    def get_best_move(self, board):
        board_string = "\n".join([" ".join(map(str, row)) for row in board])
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": (
                    "You are a Connect 4 game assistant. Respond with the best column (1 to 7) "
                    "for the next move. Ensure your message only contains the number of the "
                    "column the next move should go into, and nothing more. Your goal is to win "
                    "the game by placing 4 pieces in a row, either horizontally, diagonally, or "
                    "vertically."
                    ),
                },
                {
                    "role": "user", 
                    "content": (
                    f"The current board state is:\n{board_string}\n 0 represents a blank "
                    "space, 1 represents your opponent's piece, and 2 represents your piece. "
                    "If a column is full, do not place a piece there. What is the best column "
                    "to drop the next piece?"
                    )
                }
            ]
        )
        print(board_string)
        suggested_move = response.choices[0].message['content'].strip()
        if suggested_move.isdigit() and 1 <= int(suggested_move) <= 7:
            print(int(suggested_move))
            return int(suggested_move) - 1
        raise ValueError("Invalid move received from AI.")
