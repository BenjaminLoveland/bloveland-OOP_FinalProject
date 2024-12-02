"""
App module to run the Connect Four Applications
"""

from flask import Flask, render_template, request, jsonify
from game import Game
from ai import ConnectFourAI

app = Flask(__name__)
game = Game()
ai = ConnectFourAI(api_key="CONTACT_BEN_FOR_API_KEY")


@app.route('/')
def index():
    """
    Renders the index page for the connect Four game.
    """
    return render_template('index.html')


@app.route('/start-game', methods=['POST'])
def start_game():
    """
    Starts a new connect Four game.
    """
    try:
        game.reset_board()
        return jsonify({"message": "New game started!", "board": game.board})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get-move', methods=['POST'])
def get_move():
    """
    Calculates and uses AI's best move based on board.
    """
    try:
        data = request.json
        if not data or "board" not in data:
            return jsonify({"error": "Invalid board data"}), 400

        game.board = data['board']
        col_index = ai.get_best_move(game.board)
        if game.is_column_full(col_index):
            return jsonify({"error": "AI suggested a full column"}), 500

        game.make_move(col_index)
        winner = game.check_winner()
        if winner != 0:
            return jsonify({"winner": winner})

        return jsonify({"move": col_index + 1})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/check-winner', methods=['POST'])
def check_winner():
    """
    Checks if there is a winner in the current game.
    """
    try:
        data = request.json
        if not data or "board" not in data:
            return jsonify({"error": "Invalid board data"}), 400

        game.board = data['board']
        winner = game.check_winner()
        return jsonify({"winner": winner})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    """
    Runs the program in debug mode.
    """
    app.run(debug=True)
