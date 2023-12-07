document.addEventListener("DOMContentLoaded", function () {
    const board = document.getElementById("game-board");
    const GRID_SIZE = 4;
    const tiles = new Array(GRID_SIZE);
    let turn = 0
    let blind_turns = 0
    let blind = false
    let tile_bonus = false

    function initializeBoard() {
        for (let i = 0; i < GRID_SIZE; i++) {
            tiles[i] = new Array(GRID_SIZE);
            for (let j = 0; j < GRID_SIZE; j++) {
                tiles[i][j] = 0;
            }
        }
        addRandomTile();
        addRandomTile();
        updateBoard();
    }

    function addRandomTile() {
        const emptyTiles = [];
        for (let i = 0; i < GRID_SIZE; i++) {
            for (let j = 0; j < GRID_SIZE; j++) {
                if (tiles[i][j] === 0) {
                    emptyTiles.push({ row: i, col: j });
                }
            }
        }

        if (emptyTiles.length > 0) {
            const randomTile = emptyTiles[Math.floor(Math.random() * emptyTiles.length)];
            const value = Math.random() < 0.9 ? 2 : 4;
            tiles[randomTile.row][randomTile.col] = value;
        }
    }

    function addQmTile() {
        const emptyTiles = [];
        for (let i = 0; i < GRID_SIZE; i++) {
            for (let j = 0; j < GRID_SIZE; j++) {
                if (tiles[i][j] === 0) {
                    emptyTiles.push({ row: i, col: j });
                }
            }
        }

        if (emptyTiles.length > 0) {
            const randomTile = emptyTiles[Math.floor(Math.random() * emptyTiles.length)];
            const value = 1;
            tiles[randomTile.row][randomTile.col] = value;
        }
    }

    function qmBonus(tile) {
        switch (Math.floor(Math.random() * 2)){
            case 0:
                tile *= 2;
                return tile;
            case 1:
                tile /= 2;
                return (tile < 2) ? 0 : tile;
        }
    }

    function updateBoard() {
        board.innerHTML = "";
        for (let i = 0; i < GRID_SIZE; i++) {
            for (let j = 0; j < GRID_SIZE; j++) {
                const tileValue = tiles[i][j];
                const tile = document.createElement("div");
                tile.className = "tile";
                if(blind){
                    tile.style.background = tileValue > 0 ? getTileColor(2) : getTileColor(0);
                }
                else{
                    if(tileValue === 1){
                        tile.textContent = "?";
                        tile.style.color = "white";
                        tile.style.background = getTileColor(tileValue);
                    }
                    else{
                        tile.textContent = tileValue > 0 ? tileValue : "";
                        tile.style.background = getTileColor(tileValue);
                    }
                }
                board.appendChild(tile);
            }
        }
    }

    function getTileColor(value) {
        const colors = {
            1: "#000000",
            2: "#EEE4DA",
            4: "#EDE0C8",
            8: "#F2B179",
            16: "#F59563",
            32: "#F67C5F",
            64: "#F65E3B",
            128: "#EDCF72",
            256: "#EDCC61",
            512: "#EDC850",
            1024: "#EDC53F",
            2048: "#EDC22E",
        };
        return colors[value] || "#CDC1B4";
    }

    function isGameOver() {
        for (let i = 0; i < GRID_SIZE; i++) {
            for (let j = 0; j < GRID_SIZE; j++) {
                if (tiles[i][j] === 0) {
                    return false;
                }
                if (i > 0 && tiles[i][j] === tiles[i - 1][j]) {
                    return false;
                }
                if (i < GRID_SIZE - 1 && tiles[i][j] === tiles[i + 1][j]) {
                    return false;
                }
                if (j > 0 && tiles[i][j] === tiles[i][j - 1]) {
                    return false;
                }
                if (j < GRID_SIZE - 1 && tiles[i][j] === tiles[i][j + 1]) {
                    return false;
                }
            }
        }
        return true;
    }

    function isGameWon() {
        for (let i = 0; i < GRID_SIZE; i++) {
            for (let j = 0; j < GRID_SIZE; j++) {
                if (tiles[i][j] === 2048) {
                    return true;
                }
            }
        }
        return false;
    }

    function moveUp() {
        let moved = false;
        
        for (let col = 0; col < GRID_SIZE; col++) {
            for (let row = 1; row < GRID_SIZE; row++) {
                if (tiles[row][col] === 1) {
                    for (let i = row; i > 0; i--) {
                        if (tiles[i - 1][col] === 0) {
                            // Переместить плитку вверх
                            tiles[i - 1][col] = tiles[i][col];
                            tiles[i][col] = 0;
                            moved = true;
                        } else {
                            // Объединить плитки
                            tiles[i - 1][col] = qmBonus(tiles[i - 1][col])
                            tiles[i][col] = 0;
                            moved = true;
                            // Добавьте счет здесь, если это необходимо
                            break;
                        }
                    }
                }
                else if (tiles[row][col] !== 0) {
                    for (let i = row; i > 0; i--) {
                        if (tiles[i - 1][col] === 0) {
                            // Переместить плитку вверх
                            tiles[i - 1][col] = tiles[i][col];
                            tiles[i][col] = 0;
                            moved = true;
                        } else if (tiles[i - 1][col] === 1){
                            // Объединить плитки
                            tiles[i - 1][col] = qmBonus(tiles[i - 1][col])
                            tiles[i][col] = 0;
                            moved = true;
                        } else if (tiles[i - 1][col] === tiles[i][col]) {
                            // Объединить плитки
                            tiles[i - 1][col] *= 2;
                            tiles[i][col] = 0;
                            moved = true;
                            // Добавьте счет здесь, если это необходимо
                            break;
                        }
                    }
                }
            }
        }
        
        return moved;
    }

    function moveDown() {
        let moved = false;
    
        for (let col = 0; col < GRID_SIZE; col++) {
            for (let row = GRID_SIZE - 2; row >= 0; row--) {
                if (tiles[row][col] === 1) {
                    for (let i = row; i < GRID_SIZE - 1; i++) {
                        if (tiles[i + 1][col] === 0) {
                            // Переместить плитку вниз
                            tiles[i + 1][col] = tiles[i][col];
                            tiles[i][col] = 0;
                            moved = true;
                        } else {
                            // Объединить плитки
                            tiles[i + 1][col] = qmBonus(tiles[i + 1][col])
                            tiles[i][col] = 0;
                            moved = true;
                            // Добавьте счет здесь, если это необходимо
                            break;
                        }
                    }
                }
                else if (tiles[row][col] !== 0) {
                    for (let i = row; i < GRID_SIZE - 1; i++) {
                        if (tiles[i + 1][col] === 0) {
                            // Переместить плитку вниз
                            tiles[i + 1][col] = tiles[i][col];
                            tiles[i][col] = 0;
                            moved = true;
                        } else if (tiles[i + 1][col] === 1){
                            // Объединить плитки
                            tiles[i + 1][col] = qmBonus(tiles[i + 1][col])
                            tiles[i][col] = 0;
                            moved = true;
                        } else if (tiles[i + 1][col] === tiles[i][col]) {
                            // Объединить плитки
                            tiles[i + 1][col] *= 2;
                            tiles[i][col] = 0;
                            moved = true;
                            // Добавьте счет здесь, если это необходимо
                            break;
                        }
                    }
                }
            }
        }
    
        return moved;
    }

    function moveLeft() {
        let moved = false;
    
        for (let row = 0; row < GRID_SIZE; row++) {
            for (let col = 1; col < GRID_SIZE; col++) {
                if (tiles[row][col] === 1) {
                    for (let i = col; i > 0; i--) {
                        if (tiles[row][i - 1] === 0) {
                            // Переместить плитку влево
                            tiles[row][i - 1] = tiles[row][i];
                            tiles[row][i] = 0;
                            moved = true;
                        } else {
                            // Объединить плитки
                            tiles[row][i - 1] = qmBonus(tiles[row][i - 1])
                            tiles[row][i] = 0;
                            moved = true;
                            // Добавьте счет здесь, если это необходимо
                            break;
                        }
                    }
                }
                else if (tiles[row][col] !== 0) {
                    for (let i = col; i > 0; i--) {
                        if (tiles[row][i - 1] === 0) {
                            // Переместить плитку влево
                            tiles[row][i - 1] = tiles[row][i];
                            tiles[row][i] = 0;
                            moved = true;
                        } else if (tiles[row][i - 1] === 1){
                            // Объединить плитки
                            tiles[row][i - 1] = qmBonus(tiles[row][i - 1])
                            tiles[row][i] = 0;
                            moved = true;
                        } else if (tiles[row][i - 1] === tiles[row][i]) {
                            // Объединить плитки
                            tiles[row][i - 1] *= 2;
                            tiles[row][i] = 0;
                            moved = true;
                            // Добавьте счет здесь, если это необходимо
                            break;
                        }
                    }
                }
            }
        }
    
        return moved;
    }

    function moveRight() {
        let moved = false;

        for (let row = 0; row < GRID_SIZE; row++) {
            for (let col = GRID_SIZE - 2; col >= 0; col--) {
                if (tiles[row][col] === 1) {
                    for (let i = col; i < GRID_SIZE - 1; i++) {
                        if (tiles[row][i + 1] === 0) {
                            // Переместить плитку влево
                            tiles[row][i + 1] = tiles[row][i];
                            tiles[row][i] = 0;
                            moved = true;
                        } else {
                            // Объединить плитки
                            tiles[row][i + 1] = qmBonus(tiles[row][i + 1])
                            tiles[row][i] = 0;
                            moved = true;
                            // Добавьте счет здесь, если это необходимо
                            break;
                        }
                    }
                }
                else if (tiles[row][col] !== 0) {
                    for (let i = col; i < GRID_SIZE - 1; i++) {
                        if (tiles[row][i + 1] === 0) {
                            // Переместить плитку вправо
                            tiles[row][i + 1] = tiles[row][i];
                            tiles[row][i] = 0;
                            moved = true;
                        } else if (tiles[row][i + 1] === 1){
                            // Объединить плитки
                            tiles[row][i + 1] = qmBonus(tiles[row][i + 1])
                            tiles[row][i] = 0;
                            moved = true;
                        } else if (tiles[row][i + 1] === tiles[row][i]) {
                            // Объединить плитки
                            tiles[row][i + 1] *= 2;
                            tiles[row][i] = 0;
                            moved = true;
                            // Добавьте счет здесь, если это необходимо
                            break;
                        }
                    }
                }
            }
        }

        return moved;
    }

    function doBonus() {
        switch (Math.floor(Math.random() * 3.1)){
            case 0:
                alert("Bonux");
                addQmTile();
                updateBoard()
                break;
            case 1:
                alert("You are blinded");
                blind = true;
                blind_turns = 5 //ходов вслепую
                updateBoard()
                break;
            case 2:
                alert("freeze");
                tile_bonus = true;
                break;
            default:
                alert("no bonus");
        }
    }
    initializeBoard();


    document.addEventListener("keydown", (event) => {
        let moved = false;

        switch (event.key) {
            case "ArrowUp":
                moved = moveUp();
                break;
            case "ArrowDown":
                moved = moveDown();
                break;
            case "ArrowLeft":
                moved = moveLeft();
                break;
            case "ArrowRight":
                moved = moveRight();
                break;
        }

        if (moved) {
            turn += 1
            if(blind_turns > 0){
                blind_turns -= 1;
                if(blind_turns == 0){
                    blind = false
                }
            }

            if(!tile_bonus){
                addRandomTile();
            }
            else{
                tile_bonus = false
            }

            updateBoard();

        

            setTimeout(function () {
                if (isGameWon()) {
                    alert("You win");
                } else if (isGameOver()) {
                    alert("Game over");
                    initializeBoard();
                }

                if (turn % 10 === 0){
                    doBonus()
                }
            }, 0);
        }
    });
});
