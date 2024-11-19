document.getElementById('startGame').addEventListener('click', () => {
    // Send a POST request to the backend to start a new game
    fetch('/start-game', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // "New game started!"
        document.getElementById('gameStatus').innerText = data.message;
    });
});
