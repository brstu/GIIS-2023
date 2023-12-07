document.addEventListener("DOMContentLoaded", function () {
    const board = document.getElementById("game-board");
    const GRID_SIZE = 4;
    const tiles = Array.from({ length: GRID_SIZE }, () => Array(GRID_SIZE).fill(0));
    let turn = 0;
    let blindTurns = 0;
    let blind = false;
    let tileBonus = false;

    function initializeBoard() {
        addRandomTile();
        addRandomTile();
        updateBoard();
    }

    function addRandomTile() {
        const emptyTiles = [];
        tiles.forEach((row, i) => {
            row.forEach((value, j) => {
                if (value === 0) {
                    emptyTiles.push({ row: i, col: j });
                }
            });
        });

        if (emptyTiles.length > 0) {
            const randomTile = emptyTiles[Math.floor(Math.random() * emptyTiles.length)];
            const value = Math.random() < 0.9 ? 2 : 4;
            tiles[randomTile.row][randomTile.col] = value;
        }
    }

    function addQmTile() {
        const emptyTiles = [];
        tiles.forEach((row, i) => {
            row.forEach((value, j) => {
                if (value === 0) {
                    emptyTiles.push({ row: i, col: j });
                }
            });
        });

        if (emptyTiles.length > 0) {
            const randomTile = emptyTiles[Math.floor(Math.random() * emptyTiles.length)];
            tiles[randomTile.row][randomTile.col] = 1;
        }
    }

    function qmBonus(tile) {
        switch (Math.floor(Math.random() * 2)) {
            case 0:
                tile *= 2;
                return tile;
            case 1:
                tile /= 2;
                return tile < 2 ? 0 : tile;
        }
    }

    function updateBoard() {
        board.innerHTML = "";
        tiles.forEach((row, i) => {
            row.forEach((tileValue, j) => {
                const tile = document.createElement("div");
                tile.className = "tile";
                if (blind) {
                    tile.style.background = tileValue > 0 ? getTileColor(2) : getTileColor(0);
                } else {
                    if (tileValue === 1) {
                        tile.textContent = "?";
                        tile.style.color = "white";
                        tile.style.background = getTileColor(tileValue);
                    } else {
                        tile.textContent = tileValue > 0 ? tileValue : "";
                        tile.style.background = getTileColor(tileValue);
                    }
                }
                board.appendChild(tile);
            });
        });
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
        return tiles.some((row) => row.includes(2048));
    }

    function moveUp() {
        let moved = false;

        for (let col = 0; col < GRID_SIZE; col++) {
            for (let row = 1; row < GRID_SIZE; row++) {
                if (tiles[row][col] === 1) {
                    for (let i = row; i > 0; i--) {
                        handleMove(i, col, i - 1, col);
                        moved = true;
                    }
                } else if (tiles[row][col] !== 0) {
                    for (let i = row; i > 0; i--) {
                        handleMoveWithMerge(i, col, i - 1, col);
                        moved = true;
                        break;
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
                        handleMove(i, col, i + 1, col);
                        moved = true;
                    }
                } else if (tiles[row][col] !== 0) {
                    for (let i = row; i < GRID_SIZE - 1; i++) {
                        handleMoveWithMerge(i, col, i + 1, col);
                        moved = true;
                        break;
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
                        handleMove(row, i, row, i - 1);
                        moved = true;
                    }
                } else if (tiles[row][col] !== 0) {
                    for (let i = col; i > 0; i--) {
                        handleMoveWithMerge(row, i, row, i - 1);
                        moved = true;
                        break;
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
                        handleMove(row, i, row, i + 1);
                        moved = true;
                    }
                } else if (tiles[row][col] !== 0) {
                    for (let i = col; i < GRID_SIZE - 1; i++) {
                        handleMoveWithMerge(row, i, row, i + 1);
                        moved = true;
                        break;
                    }
                }
            }
        }

        return moved;
    }

    function handleMove(row, col, newRow, newCol) {
        tiles[newRow][newCol] = tiles[row][col];
        tiles[row][col] = 0;
    }

    function handleMoveWithMerge(row, col, newRow, newCol) {
        if (tiles[newRow][newCol] === 0) {
            handleMove(row, col, newRow, newCol);
        } else if (tiles[newRow][newCol] === 1) {
            tiles[newRow][newCol] = qmBonus(tiles[newRow][newCol]);
            tiles[row][col] = 0;
        } else if (tiles[newRow][newCol] === tiles[row][col]) {
            tiles[newRow][newCol] *= 2;
            tiles[row][col] = 0;
        }
    }

    function doBonus() {
        switch (Math.floor(Math.random() * 4)) {
            case 0:
                alert("Bonus");
                addQmTile();
                updateBoard();
                break;
            case 1:
                alert("You are blinded");
                blind = true;
                blindTurns = 5; // Number of turns blinded
                updateBoard();
                break;
            case 2:
                alert("Freeze");
                tileBonus = true;
                break;
            default:
                alert("No bonus");
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
            turn += 1;
            if (blindTurns > 0) {
                blindTurns -= 1;
                if (blindTurns === 0) {
                    blind = false;
                }
            }

            if (!tileBonus) {
                addRandomTile();
            } else {
                tileBonus = false;
            }

            updateBoard();

            setTimeout(function () {
                if (isGameWon()) {
                    alert("You win!");
                } else if (isGameOver()) {
                    alert("Game over");
                    initializeBoard();
                }

                if (turn % 10 === 0) {
                    doBonus();
                }
            }, 0);
        }
    });
});
