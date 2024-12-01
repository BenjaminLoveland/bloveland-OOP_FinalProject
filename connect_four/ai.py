"""
AI module to handle interactions with chatGPT
Note: I currently have some parts commented and
replaced so that I don't need the api key to test
features.
"""

# import openai  # Comment this out if not using OpenAI


class ConnectFourAI:
    def __init__(self, api_key):
        # Temporarily disable API key setup
        # openai.api_key = api_key
        self.api_key = api_key  # Keep this as a placeholder if needed

    def get_best_move(self, board):
        # Mock AI behavior since OpenAI interaction is disabled
        print("Mocking AI move. Returning the first non-full column.")

        # Simulate AI logic: choose the first non-full column
        for col_index in range(len(board[0])):
            if any(row[col_index] == 0 for row in board):
                return col_index  # Return the first valid column
        raise ValueError("No valid moves left.")

        # Uncomment and use this code when you have the API key:
        # board_string = "\n".join([" ".join(map(str, row)) for row in board])
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content":
        #  "You are a Connect 4 game assistant..."},
        #         {"role": "user", "content":
        #  f"The current board state is:\n{board_string}\n..."}
        #     ]
        # )
        # suggested_move = response.choices[0].message['content'].strip()
        # if suggested_move.isdigit() and 1 <= int(suggested_move) <= 7:
        #     return int(suggested_move) - 1
        # raise ValueError("Invalid move received from AI.")
