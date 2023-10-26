const gridContainer = document.querySelector('.grid-container')
const scoreElement = document.querySelector('.score')

const bonusMessageElement = document.querySelector('.bonus-message')
const gridSize = 4
let grid = new Array(gridSize).fill(null).map(() => new Array(gridSize).fill(0))
let score = 0
let bonusActive = false
let isGameOver = false

// Функция для обновления отображения времени бонуса
function updateBonusTimerDisplay(seconds) {
  bonusTimerElement.textContent = `Bonus Timer: ${seconds}s`
}

function initializeGame() {
  grid = new Array(gridSize).fill(null).map(() => new Array(gridSize).fill(0))
  score = 0
  bonusActive = false
  updateGridDisplay()
  updateScoreDisplay()
  addRandomTile()
  addRandomTile()
}

function updateGridDisplay() {
  gridContainer.innerHTML = ''
  for (let i = 0; i < gridSize; i++) {
    for (let j = 0; j < gridSize; j++) {
      const cellValue = grid[i][j]
      const gridCell = document.createElement('div')
      gridCell.classList.add('grid-cell')
      gridCell.textContent = cellValue > 0 ? cellValue : ''
      gridCell.style.background = getTileColor(cellValue)
      gridContainer.appendChild(gridCell)
    }
  }
}

function updateScoreDisplay() {
  scoreElement.textContent = `Score: ${score}`
}

function addRandomTile() {
  const availableCells = []
  for (let i = 0; i < gridSize; i++) {
    for (let j = 0; j < gridSize; j++) {
      if (grid[i][j] === 0) {
        availableCells.push({ row: i, col: j })
      }
    }
  }

  if (availableCells.length > 0) {
    const randomValue = window.crypto.getRandomValues(new Uint32Array(1))[0] / 0xFFFFFFFF;
    const randomIndex = Math.floor(randomValue * availableCells.length);
    const randomCell = availableCells[randomIndex];
    grid[randomCell.row][randomCell.col] = randomValue < 0.9 ? 2 : 4;
  }
  updateGridDisplay()
}

function getTileColor(value) {
  switch (value) {
    case 2:
      return '#eee4da'
    case 4:
      return '#ede0c8'
    case 8:
      return '#f2b179'
    case 16:
      return '#f59563'
    case 32:
      return '#f67c5f'
    case 64:
      return '#f65e3b'
    case 128:
      return '#edcf72'
    case 256:
      return '#edcc61'
    case 512:
      return '#edc850'
    case 1024:
      return '#edc53f'
    case 2048:
      return '#edc22e'
    default:
      return '#3c3a32' // Цвет по умолчанию
  }
}

function activateBonusLeft() {
  if (!bonusActive) {
    bonusActive = true
    bonusTimerElement.style.color = 'green'
    bonusMessageElement.style.display = 'block'
  }
}

function deactivateBonusLeft() {
  if (bonusActive) {
    bonusActive = false
    bonusTimerElement.style.color = 'black'
    bonusMessageElement.style.display = 'none'
  }
}

document.addEventListener('keydown', (event) => {
  if (isGameOver) {
    return
  }

  if (event.key === 'ArrowLeft') {
    moveLeft()
  } else if (event.key === 'ArrowRight') {
    moveRight()
  } else if (event.key === 'ArrowUp') {
    moveUp()
  } else if (event.key === 'ArrowDown') {
    moveDown()
  } else {
    return
  }
  addRandomTile()
  updateGridDisplay()
  updateScoreDisplay()

  if (checkGameOver()) {
    endGame()
  }
})

// Логика движения влево
function moveLeft() {
  for (let i = 0; i < gridSize; i++) {
    for (let j = 1; j < gridSize; j++) {
      if (grid[i][j] > 0) {
        shiftLeft(i, j);
      }
    }
  }
}

function shiftLeft(row, col) {
  while (col > 0) {
    if (grid[row][col - 1] === 0) {
      moveBlockLeft(row, col, row, col - 1);
      col--;
    } else if (grid[row][col - 1] === grid[row][col]) {
      mergeBlocksLeft(row, col, row, col - 1);
      col = 0;
    } else {
      break;
    }
  }
}

function moveBlockLeft(fromRow, fromCol, toRow, toCol) {
  grid[toRow][toCol] = grid[fromRow][fromCol];
  grid[fromRow][fromCol] = 0;
}

function mergeBlocksLeft(row1, col1, row2, col2) {
  if (grid[row1][col1] === 16) {
    bonusActive = true;
    score += 100;
    activateBonusLeft();
    showBonusMessage();
  }

  grid[row2][col2] *= 2;
  score += grid[row2][col2];
  grid[row1][col1] = 0;
}

// Логика движения вправо
function moveRight() {
  for (let i = 0; i < gridSize; i++) {
    for (let j = gridSize - 2; j >= 0; j--) {
      if (grid[i][j] > 0) {
        shiftRight(i, j);
      }
    }
  }
}

function shiftRight(row, col) {
  while (col < gridSize - 1) {
    if (grid[row][col + 1] === 0) {
      moveBlockRight(row, col, row, col + 1);
      col++;
    } else if (grid[row][col + 1] === grid[row][col]) {
      mergeBlocksUpDownRights(row, col, row, col + 1);
      col = gridSize - 1;
    } else {
      break;
    }
  }
}

function moveBlockRight(fromRow, fromCol, toRow, toCol) {
  grid[toRow][toCol] = grid[fromRow][fromCol];
  grid[fromRow][fromCol] = 0;
}

// Логика движения вверх
function moveUp() {
  for (let j = 0; j < gridSize; j++) {
    for (let i = 1; i < gridSize; i++) {
      if (grid[i][j] > 0) {
        shiftUp(i, j);
      }
    }
  }
}

function shiftUp(row, col) {
  while (row > 0) {
    if (grid[row - 1][col] === 0) {
      moveBlockUp(row, col, row - 1, col);
      row--;
    } else if (grid[row - 1][col] === grid[row][col]) {
      mergeBlocksUpDownRights(row, col, row - 1, col);
      row = 0;
    } else {
      break;
    }
  }
}

function moveBlockUp(fromRow, fromCol, toRow, toCol) {
  grid[toRow][toCol] = grid[fromRow][fromCol];
  grid[fromRow][fromCol] = 0;
}

function mergeBlocksUpDownRights(row1, col1, row2, col2) {
  grid[row2][col2] *= 2;
  score += grid[row2][col2];
  grid[row1][col1] = 0;
}

// Логика движения вниз
function moveDown() {
  for (let j = 0; j < gridSize; j++) {
    for (let i = gridSize - 2; i >= 0; i--) {
      if (grid[i][j] > 0) {
        shiftDown(i, j);
      }
    }
  }
}

function shiftDown(row, col) {
  while (row < gridSize - 1) {
    if (grid[row + 1][col] === 0) {
      moveBlockDown(row, col, row + 1, col);
      row++;
    } else if (grid[row + 1][col] === grid[row][col]) {
      if (grid[row][col] === 64) {
        bonusActive = true;
        duplicateTiles();
        showBonusMessage();
        return;
      } else {
        mergeBlocksUpDownRights(row, col, row + 1, col);
        return;
      }
    } else {
      break;
    }
  }
}

function moveBlockDown(fromRow, fromCol, toRow, toCol) {
  grid[toRow][toCol] = grid[fromRow][fromCol];
  grid[fromRow][fromCol] = 0;
}

// Дублирование всех карточек на игровом поле
function duplicateTiles() {
  for (let i = 0; i < gridSize; i++) {
    for (let j = 0; j < gridSize; j++) {
      if (grid[i][j] > 0) {
        grid[i][j] *= 2
      }
    }
  }
  updateGridDisplay()
}

function checkGameOver() {
  // Логика проверки окончания игры
  for (let i = 0; i < gridSize; i++) {
    for (let j = 0; j < gridSize; j++) {
      if (grid[i][j] === 0) {
        return false // Найдены пустые ячейки, игра не окончена
      }
      if (j < gridSize - 1 && grid[i][j] === grid[i][j + 1]) {
        return false // Можно объединить соседние блоки по горизонтали
      }
      if (i < gridSize - 1 && grid[i][j] === grid[i + 1][j]) {
        return false // Можно объединить соседние блоки по вертикали
      }
    }
  }
  return true // Нельзя сделать дополнительных ходов, игра окончена
}

function endGame() {
  isGameOver = true
  const gameOverText = document.getElementById('game-over-message')
  gameOverText.style.display = 'block'
  const resumeButton = document.getElementById('resume-button')
  resumeButton.style.display = 'block'
}

document.getElementById('resume-button').addEventListener('click', () => {
  if (isGameOver) {
    isGameOver = false
    const resumeButton = document.getElementById('resume-button')
    resumeButton.style.display = 'none'
    const gameOverText = document.getElementById('game-over-message')
    gameOverText.style.display = 'none'
    initializeGame()
  }
})

function showBonusMessage() {
  bonusMessageElement.style.display = 'block'
  setTimeout(() => {
    bonusMessageElement.style.display = 'none'
  }, 1000)
}

initializeGame()
