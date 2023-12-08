import Grid from "./Grid.js"
import Tile from "./Tile.js"

const gameBoard = document.getElementById("game-board")

const grid = new Grid(gameBoard)
grid.randomEmptyCell().tile = new Tile(gameBoard)
grid.randomEmptyCell().tile = new Tile(gameBoard)
setupInput()

function setupInput() {
  window.addEventListener("keydown", handleInputOnce);
}

function handleInputOnce(e) {
  window.removeEventListener("keydown", handleInputOnce);
  handleInput(e).then(setupInput);
}

function move(direction) {
  return new Promise((resolve) => {
    if (canMove(direction)) {
      resolve();
      moveTiles(direction);
      grid.cells.forEach((cell) => cell.mergeTiles());
      const newTile = new Tile(gameBoard);
      grid.randomEmptyCell().tile = newTile;
    }
  });
}

function handleInput(e) {
  return new Promise(async (resolve) => {
    try {
      switch (e.key) {
        case "ArrowUp":
          await move("up");
          break;
        case "ArrowDown":
          await move("down");
          break;
        case "ArrowLeft":
          await move("left");
          break;
        case "ArrowRight":
          await move("right");
          break;
        default:
          return;
      }

      if (!canMove("up") && !canMove("down") && !canMove("left") && !canMove("right")) {
        await showLoseAlert();
      }
    } catch (err) {
      console.error(err);
    } finally {
      resolve();
    }
  });
}

async function showLoseAlert() {
  await newTile.waitForTransition(true);
  alert("You lose");
}

function moveUp() {
  return slideTiles(grid.cellsByColumn)
}

function moveDown() {
  return slideTiles(grid.cellsByColumn.map(column => [...column].reverse()))
}

function moveLeft() {
  return slideTiles(grid.cellsByRow)
}

function moveRight() {
  return slideTiles(grid.cellsByRow.map(row => [...row].reverse()))
}

function slideTiles(cells) {
  return Promise.all(
    cells.flatMap(group => {
      const promises = []
      for (let i = 1; i < group.length; i++) {
        const cell = group[i]
        if (cell.tile == null) continue
        let lastValidCell
        for (let j = i - 1; j >= 0; j--) {
          const moveToCell = group[j]
          if (!moveToCell.canAccept(cell.tile)) break
          lastValidCell = moveToCell
        }

        if (lastValidCell != null) {
          promises.push(cell.tile.waitForTransition())
          if (lastValidCell.tile != null) {
            lastValidCell.mergeTile = cell.tile
          } else {
            lastValidCell.tile = cell.tile
          }
          cell.tile = null
        }
      }
      return promises
    })
  )
}

function canMoveUp() {
  return canMove(grid.cellsByColumn)
}

function canMoveDown() {
  return canMove(grid.cellsByColumn.map(column => [...column].reverse()))
}

function canMoveLeft() {
  return canMove(grid.cellsByRow)
}

function canMoveRight() {
  return canMove(grid.cellsByRow.map(row => [...row].reverse()))
}

function canMove(cells) {
  return cells.some(group => {
    return group.some((cell, index) => {
      if (index === 0) return false
      if (cell.tile == null) return false
      const moveToCell = group[index - 1]
      return moveToCell.canAccept(cell.tile)
    })
  })
}
