let board = [];
let currentPlayer = 1;
let gameActive = true;

function renderBoard() {
    console.log(`Rendering board... Current Player: ${currentPlayer === 1 ? "Player" : "ChatGPT"}`);
    const boardContainer = document.getElementById('board');
    boardContainer.innerHTML = '';

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

            if (currentPlayer === 1 && cell === 0 && gameActive) {
                cellDiv.addEventListener('click', () => handlePlayerMove(colIndex));
            }

            boardContainer.appendChild(cellDiv);
        });
    });

    console.log("Board rendered successfully.");
}

function handlePlayerMove(colIndex) {
    if (!gameActive || currentPlayer !== 1) {
        alert("It's not your turn or the game is over!");
        return;
    }

    if (makeMove(colIndex, 1)) {
        renderBoard();
        checkWinner().then(winner => {
            if (!winner && gameActive) {
                currentPlayer = 2;
                console.log("Player has moved. Passing turn to ChatGPT...");
                fetchChatGPTMove();
            }
        });
    } else {
        alert('This column is full! Choose a different one.');
    }
}

function makeMove(colIndex, player) {
    for (let row = board.length - 1; row >= 0; row--) {
        if (board[row][colIndex] === 0) {
            board[row][colIndex] = player;
            return true;
        }
    }
    return false;
}

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

            const colIndex = data.move - 1;
            if (makeMove(colIndex, 2)) {
                renderBoard();
                checkWinner().then(winner => {
                    if (!winner && gameActive) {
                        currentPlayer = 1;
                        console.log("ChatGPT has moved. Player's turn...");
                    }
                });
            } else {
                console.error(`ChatGPT tried to place a piece in column ${colIndex + 1}, which is full.`);
                console.error(`ChatGPT's response: ${data.chatGPTResponse}`);
                alert('ChatGPT attempted to place a piece in a full column!');
                currentPlayer = 1;
            }
        })
        .catch(error => {
            console.error('Error fetching move from ChatGPT:', error);
            currentPlayer = 1;
        });
    currentPlayer = 1;
}

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
                gameActive = false;
                return true;
            }
            return false;
        })
        .catch(error => {
            console.error('Error checking for winner:', error);
            return false;
        });
}

document.getElementById('startGame').addEventListener('click', () => {
    fetch('/start-game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            console.log("New game started:", data.board);
            board = data.board;
            currentPlayer = 1;
            gameActive = true;
            document.getElementById('gameStatus').innerText = data.message;
            renderBoard();
        })
        .catch(error => console.error('Error starting new game:', error));
});

// Render initial empty board
renderBoard();
