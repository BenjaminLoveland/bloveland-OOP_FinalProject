let board = []; // Game board
let currentPlayer = 1; // Player 1 starts

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

            // Allow player interaction only if it's their turn
            if (currentPlayer === 1 && cell === 0) {
                cellDiv.addEventListener('click', () => handlePlayerMove(colIndex));
            }

            boardContainer.appendChild(cellDiv);
        });
    });

    console.log("Board rendered successfully.");
}


// Handle player move
function handlePlayerMove(colIndex) {
    if (currentPlayer !== 1) {
        alert("It's not your turn!");
        return;
    }

    for (let row = board.length - 1; row >= 0; row--) {
        if (board[row][colIndex] === 0) {
            board[row][colIndex] = 1; // Player 1 places a piece
            renderBoard();

            // Pass the turn to ChatGPT
            currentPlayer = 2;
            console.log("Player has moved. Passing turn to ChatGPT...");
            fetchChatGPTMove(); // Fetch ChatGPT's move
            return;
        }
    }

    alert('This column is full! Choose a different one.');
}

// Fetch ChatGPT's move
function fetchChatGPTMove() {
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

            const colIndex = data.move - 1; // Convert 1-based column to 0-based index
            placeChatGPTMove(colIndex, data.chatGPTResponse); // Pass ChatGPT's response
        })
        .catch(error => {
            console.error('Error fetching move from ChatGPT:', error);
        });
}

function placeChatGPTMove(colIndex, chatGPTResponse) {
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
    console.error(`ChatGPT's response: ${chatGPTResponse}`);
    alert('ChatGPT attempted to place a piece in a full column!');
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
            document.getElementById('gameStatus').innerText = data.message;
            renderBoard(); // Render the initial game board
        })
        .catch(error => console.error('Error starting new game:', error));
});

// Render initial empty board
renderBoard();
