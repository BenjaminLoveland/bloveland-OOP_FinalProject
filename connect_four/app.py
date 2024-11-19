
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Route to serve the main page
@app.route('/')
def index():
    return render_template('index.html')

# API to start a new game
@app.route('/start-game', methods=['POST'])
def start_game():
    return jsonify({"message": "New game started!"})

if __name__ == '__main__':
    app.run(debug=True)
