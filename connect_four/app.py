from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "CONTACT_BEN_FOR_API_KEY"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-game', methods=['POST'])
def start_game():
    try:
        initial_board = [[0 for _ in range(7)] for _ in range(6)]
        print("New game started with board:", initial_board)
        return jsonify({"message": "New game started!", "board": initial_board})
    except Exception as e:
        print(f"Error during /start-game: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/get-move', methods=['POST'])
def get_move():
    try:
        data = request.json
        if not data or "board" not in data:
            return jsonify({"error": "Invalid or missing board data"}), 400

        board_state = data["board"]
        print("Board state received:", board_state)

        # Convert the board to a string representation for ChatGPT
        board_string = "\n".join([" ".join(map(str, row)) for row in board_state])

        # Query OpenAI for the next move
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Connect 4 game assistant. Respond with the best column (1 to 7) for the next move. Ensure your message only contains the number of the column the next move should go into, and nothing more."},
                {"role": "user", "content": f"The current board state is:\n{board_string}\n 0 represents a blank space, 1 represents your opponent's piece, and 2 represents your piece. If a column is full, do not place a piece there. What is the best column to drop the next piece?"}
            ]
        )

        # Extract the suggested move from ChatGPT's response
        suggested_move = response.choices[0].message['content'].strip()
        print("ChatGPT suggested move:", suggested_move)

        # Validate the suggested move
        if not suggested_move.isdigit() or not (1 <= int(suggested_move) <= 7):
            print("Invalid move received from ChatGPT.")
            return jsonify({"error": "Invalid move received from ChatGPT", "chatGPTResponse": suggested_move}), 500

        col_index = int(suggested_move) - 1
        if all(row[col_index] != 0 for row in board_state):
            print("ChatGPT suggested a full column.")
            return jsonify({"error": "ChatGPT suggested a full column", "chatGPTResponse": suggested_move}), 500

        return jsonify({"move": col_index + 1, "chatGPTResponse": suggested_move})  # Return 1-based column

    except Exception as e:
        print(f"Error during /get-move: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
