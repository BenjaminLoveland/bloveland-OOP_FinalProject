let board = []; // Game board
let currentPlayer = 1; // Player 1 starts
let gameActive = true; // Track if the game is still active

// Render the game board
function renderBoard() {
    console.log(`Rendering board... Current Player: ${currentPlayer === 1 ? "Player" : "ChatGPT"}`);
    const boardContainer = document.getElementById('board');
    boardContainer.innerHTML = ''; // Clear the board

    board.forEach((row, rowIndex) => {
        row.forEach((cell, colIndex) => {
            const cellDiv = document.createElement('div');
            cellDiv.className = 'cell';
            cellDiv.dataset.row = rowIndex;
            cellDiv.dataset.col = colIndex;

            if (cell === 1) {
                cellDiv.classList.add('player1');
            } else if (cell === 2) {
                cellDiv.classList.add('player2');
            }

            // Allow player interaction only if it's their turn and game is active
            if (currentPlayer === 1 && cell === 0 && gameActive) {
                cellDiv.addEventListener('click', () => handlePlayerMove(colIndex));
            }

            boardContainer.appendChild(cellDiv);
        });
    });

    console.log("Board rendered successfully.");
}

// Handle player move
function handlePlayerMove(colIndex) {
    if (!gameActive || currentPlayer !== 1) {
        alert("It's not your turn or the game is over!");
        return;
    }

    if (makeMove(colIndex, 1)) {
        renderBoard();
        checkWinner().then(winner => {
            if (!winner && gameActive) {
                // Pass the turn to ChatGPT
                currentPlayer = 2;
                console.log("Player has moved. Passing turn to ChatGPT...");
                fetchChatGPTMove(); // Fetch ChatGPT's move
            }
        });
    } else {
        alert('This column is full! Choose a different one.');
    }
}

// Make a move on the board
function makeMove(colIndex, player) {
    for (let row = board.length - 1; row >= 0; row--) {
        if (board[row][colIndex] === 0) {
            board[row][colIndex] = player;
            return true;
        }
    }
    return false;
}

// Fetch ChatGPT's move
function fetchChatGPTMove() {
    if (!gameActive) return;

    fetch('/get-move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ board: board })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                // Log the error and ChatGPT's response
                console.error(`Error: ${data.error}`);
                if (data.chatGPTResponse) {
                    console.error(`ChatGPT's response: ${data.chatGPTResponse}`);
                }
                alert(`Error: ${data.error}`);
                return;
            }

            if (data.winner) {
                alert('ChatGPT wins!');
                gameActive = false;
                return;
            }

            const colIndex = data.move - 1; // Convert 1-based column to 0-based index
            if (makeMove(colIndex, 2)) {
                renderBoard();
                checkWinner().then(winner => {
                    if (!winner && gameActive) {
                        currentPlayer = 1; // Switch back to Player 1's turn
                        console.log("ChatGPT has moved. Player's turn...");
                    }
                });
            } else {
                console.error(`ChatGPT tried to place a piece in column ${colIndex + 1}, which is full.`);
                console.error(`ChatGPT's response: ${data.chatGPTResponse}`);
                alert('ChatGPT attempted to place a piece in a full column!');
                currentPlayer = 1; // Switch back to Player 1 to retry
            }
        })
        .catch(error => {
            console.error('Error fetching move from ChatGPT:', error);
            currentPlayer = 1; // Switch back to Player 1 to retry
        });
    currentPlayer = 1;
}

// Check for a winner
function checkWinner() {
    return fetch('/check-winner', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ board: board })
    })
        .then(response => response.json())
        .then(data => {
            if (data.winner) {
                alert(`${data.winner === 1 ? 'Player' : 'ChatGPT'} wins!`);
                gameActive = false; // Stop the game
                return true;
            }
            return false;
        })
        .catch(error => {
            console.error('Error checking for winner:', error);
            return false;
        });
}

// Start a new game
document.getElementById('startGame').addEventListener('click', () => {
    fetch('/start-game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            console.log("New game started:", data.board);
            board = data.board; // Initialize the board
            currentPlayer = 1; // Player 1 starts
            gameActive = true; // Game is active
            document.getElementById('gameStatus').innerText = data.message;
            renderBoard(); // Render the initial game board
        })
        .catch(error => console.error('Error starting new game:', error));
});

// Render initial empty board
renderBoard();
