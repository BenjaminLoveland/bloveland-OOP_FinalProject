let board = []; // Initialize an empty board
let currentPlayer = 1; // Player 1 starts

// Function to render the game board
function renderBoard() {
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

            // Only allow player moves on empty cells
            if (currentPlayer === 1 && cell === 0) {
                cellDiv.addEventListener('click', () => handlePlayerMove(colIndex));
            }

            boardContainer.appendChild(cellDiv);
        });
    });
}

// Function to handle the player's move
function handlePlayerMove(colIndex) {
    for (let row = board.length - 1; row >= 0; row--) {
        if (board[row][colIndex] === 0) {
            board[row][colIndex] = 1; // Player 1 places a piece
            currentPlayer = 2; // Switch to ChatGPT's turn
            renderBoard();
            fetchChatGPTMove(); // Fetch ChatGPT's move
            return;
        }
    }
    alert('This column is full! Choose a different one.');
}

// Function to fetch ChatGPT's move from the backend
function fetchChatGPTMove() {
    fetch('/get-move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ board: board })
    })
        .then(response => response.json())
        .then(data => {
            const colIndex = data.move - 1; // Convert 1-based column to 0-based index
            placeChatGPTMove(colIndex); // Place ChatGPT's piece
        })
        .catch(error => console.error('Error fetching move from ChatGPT:', error));
}

// Function to place ChatGPT's move on the board
function placeChatGPTMove(colIndex) {
    for (let row = board.length - 1; row >= 0; row--) {
        if (board[row][colIndex] === 0) {
            board[row][colIndex] = 2; // ChatGPT places a piece
            currentPlayer = 1; // Switch back to Player 1's turn
            renderBoard();
            return;
        }
    }
    // Log an error if something went wrong
    console.error(`ChatGPT tried to place a piece in column ${colIndex + 1}, which is full.`);
    alert('ChatGPT attempted to place a piece in a full column!');
}

// Event listener to start a new game
document.getElementById('startGame').addEventListener('click', () => {
    fetch('/start-game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            board = data.board; // Initialize the board
            currentPlayer = 1; // Player 1 starts
            document.getElementById('gameStatus').innerText = data.message;
            renderBoard(); // Render the initial game board
        })
        .catch(error => console.error('Error starting new game:', error));
});

// Initial board rendering
renderBoard();
