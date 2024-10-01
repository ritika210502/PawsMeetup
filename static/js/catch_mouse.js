
let score = 0;
let isGameRunning = false;

document.getElementById('start-button').addEventListener('click', startGame);
document.getElementById('mouse').addEventListener('click', catchMouse);

function startGame() {
    if (!isGameRunning) {
        isGameRunning = true;
        score = 0;
        updateScore();
        moveMouse();
        document.getElementById('start-button').innerText = 'Game Running...';
    }
}

function catchMouse() {
    if (isGameRunning) {
        score++;
        updateScore();
        moveMouse();
    }
}

function updateScore() {
    document.getElementById('score').innerText = `Score: ${score}`;
}

function moveMouse() {
    const gameArea = document.getElementById('game-area');
    const mouse = document.getElementById('mouse');

    const maxX = gameArea.offsetWidth - mouse.offsetWidth;
    const maxY = gameArea.offsetHeight - mouse.offsetHeight;

    const newX = Math.floor(Math.random() * maxX);
    const newY = Math.floor(Math.random() * maxY);

    mouse.style.left = `${newX}px`;
    mouse.style.top = `${newY}px`;
}
