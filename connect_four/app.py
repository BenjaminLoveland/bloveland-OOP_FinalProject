from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "API_KEY"

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

        # Query OpenAI for the next move using the updated interface
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a Connect 4 game assistant. Respond with the best column (1 to 7) for the next move."},
                {"role": "user", "content": f"The current board state is:\n{board_string}\nWhat is the best column to drop the next piece?"}
            ]
        )

        # Extract the suggested move (column) from ChatGPT's response
        suggested_move = response['choices'][0]['message']['content'].strip()

        if not suggested_move.isdigit() or not (1 <= int(suggested_move) <= 7):
            return jsonify({"error": "Invalid move received from ChatGPT"}), 500

        col_index = int(suggested_move) - 1
        if all(row[col_index] != 0 for row in board_state):
            return jsonify({"error": "ChatGPT suggested a full column. Try again."}), 500

        return jsonify({"move": col_index + 1})  # Return 1-based column

    except Exception as e:
        print(f"Error during /get-move: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting the server: {e}")
