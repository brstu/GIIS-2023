class Game2048 {
  #gridSize;
  #grid;
  #score;
  #bonusActive;
  #isGameOver;

  constructor(gridSize, gridContainer, scoreElement, bonusMessageElement) {
    this.#gridSize = gridSize;
    this.gridContainer = gridContainer;
    this.scoreElement = scoreElement;
    this.bonusMessageElement = bonusMessageElement;
    this.initializeGame();
    document.addEventListener('keydown', event => this.handleKeyPress(event));
    document.getElementById('resume-button').addEventListener('click', () => this.resumeGame());
  }

  initializeGame() {
    this.#grid = new Array(this.#gridSize).fill(null).map(() => new Array(this.#gridSize).fill(0));
    this.#score = 0;
    this.#bonusActive = false;
    this.#isGameOver = false;
    this.updateGridDisplay();
    this.updateScoreDisplay();
    this.addRandomTile();
    this.addRandomTile();
  }

  get gridSize() {
    return this.#gridSize;
  }

  get isGameOver() {
    return this.#isGameOver;
  }

  handleKeyPress(event) {
    if (this.isGameOver) {
      return;
    }

    switch (event.key) {
      case 'ArrowLeft':
        this.moveLeft();
        break;
      case 'ArrowRight':
        this.moveRight();
        break;
      case 'ArrowUp':
        this.moveUp();
        break;
      case 'ArrowDown':
        this.moveDown();
        break;
      default:
        return;
    }

    this.addRandomTile();
    this.updateGridDisplay();
    this.updateScoreDisplay();

    if (this.checkGameOver()) {
      this.endGame();
    }
  }

  updateGridDisplay() {
    this.gridContainer.textContent = '';
    for (let i = 0; i < this.#gridSize; i++) {
      for (let j = 0; j < this.#gridSize; j++) {
        const cellValue = this.#grid[parseInt(i)][parseInt(j)];
        const gridCell = document.createElement('div');
        gridCell.classList.add('grid-cell');
        gridCell.textContent = cellValue > 0 ? cellValue : '';
        gridCell.style.background = this.getTileColor(cellValue);
        this.gridContainer.appendChild(gridCell);
      }
    }
  }

  updateScoreDisplay() {
    this.scoreElement.textContent = `Score: ${this.#score}`;
  }

  moveLeft() {
    for (let i = 0; i < this.#gridSize; i++) {
      for (let j = 1; j < this.#gridSize; j++) {
        if (this.#grid[parseInt(i)][parseInt(j)] > 0) {
          this.shiftLeft(i, j);
        }
      }
    }
  }

  shiftLeft(row, col) {
    while (col > 0) {
      if (this.#grid[parseInt(row)][parseInt(col - 1)] === 0) {
        this.moveBlockLeft(row, col, row, col - 1);
        col--;
      } else if (this.#grid[parseInt(row)][parseInt(col - 1)] === this.#grid[parseInt(row)][parseInt(col)]) {
        this.mergeBlocksLeft(row, col, row, col - 1);
        col = 0;
      } else {
        break;
      }
    }
  }

  getTileColor(value) {
    switch (value) {
      case 2:
        return '#eee4da';
      case 4:
        return '#ede0c8';
      case 8:
        return '#f2b179';
      case 16:
        return '#f59563';
      case 32:
        return '#f67c5f';
      case 64:
        return '#f65e3b';
      case 128:
        return '#edcf72';
      case 256:
        return '#edcc61';
      case 512:
        return '#edc850';
      case 1024:
        return '#edc53f';
      case 2048:
        return '#edc22e';
      default:
        return '#3c3a32'; // Цвет по умолчанию
    }
  }

  activateBonusLeft() {
    if (!this.#bonusActive) {
      this.#bonusActive = true;
      this.bonusMessageElement.style.display = 'block';
    }
  }

  moveRight() {
    for (let i = 0; i < this.#gridSize; i++) {
      for (let j = this.#gridSize - 2; j >= 0; j--) {
        if (this.#grid[parseInt(i)][parseInt(j)] > 0) {
          this.shiftRight(i, j);
        }
      }
    }
  }

  shiftRight(row, col) {
    while (col < this.#gridSize - 1) {
      if (this.#grid[parseInt(row)][parseInt(col + 1)] === 0) {
        this.moveBlockRight(row, col, row, col + 1);
        col++;
      } else if (this.#grid[parseInt(row)][parseInt(col + 1)] === this.#grid[parseInt(row)][parseInt(col)]) {
        this.mergeBlocksUpDownRight(row, col, row, col + 1);
        col = this.#gridSize - 1;
      } else {
        break;
      }
    }
  }

  moveBlockRight(fromRow, fromCol, toRow, toCol) {
    this.#grid[parseInt(toRow)][parseInt(toCol)] = this.#grid[parseInt(fromRow)][parseInt(fromCol)];
    this.#grid[parseInt(fromRow)][parseInt(fromCol)] = 0;
  }

  moveUp() {
    for (let j = 0; j < this.#gridSize; j++) {
      for (let i = 1; i < this.#gridSize; i++) {
        if (this.#grid[parseInt(i)][parseInt(j)] > 0) {
          this.shiftUp(i, j);
        }
      }
    }
  }

  shiftUp(row, col) {
    while (row > 0) {
      if (this.#grid[parseInt(row - 1)][parseInt(col)] === 0) {
        this.moveBlockUp(row, col, row - 1, col);
        row--;
      } else if (this.#grid[parseInt(row - 1)][parseInt(col)] === this.#grid[parseInt(row)][parseInt(col)]) {
        this.mergeBlocksUpDownRight(row, col, row - 1, col);
        row = 0;
      } else {
        break;
      }
    }
  }

  moveBlockUp(fromRow, fromCol, toRow, toCol) {
    this.#grid[parseInt(toRow)][parseInt(toCol)] = this.#grid[parseInt(fromRow)][parseInt(fromCol)];
    this.#grid[parseInt(fromRow)][parseInt(fromCol)] = 0;
  }

  moveDown() {
    for (let j = 0; j < this.#gridSize; j++) {
      for (let i = this.#gridSize - 2; i >= 0; i--) {
        if (this.#grid[parseInt(i)][parseInt(j)] > 0) {
          this.shiftDown(i, j);
        }
      }
    }
  }

  shiftDown(row, col) {
    while (row < this.#gridSize - 1) {
      if (this.#grid[parseInt(row + 1)][parseInt(col)] === 0) {
        this.moveBlockDown(row, col, row + 1, col);
        row++;
      } else if (this.#grid[parseInt(row + 1)][parseInt(col)] === this.#grid[parseInt(row)][parseInt(col)]) {
        if (this.#grid[parseInt(row)][parseInt(col)] === 64) {
          this.#bonusActive = true;
          this.duplicateTiles();
          this.showBonusMessage();
          return;
        } else {
          this.mergeBlocksUpDownRight(row, col, row + 1, col);
          return;
        }
      } else {
        break;
      }
    }
  }

  moveBlockDown(fromRow, fromCol, toRow, toCol) {
    this.#grid[parseInt(toRow)][parseInt(toCol)] = this.#grid[parseInt(fromRow)][parseInt(fromCol)];
    this.#grid[parseInt(fromRow)][parseInt(fromCol)] = 0;
  }

  mergeBlocksUpDownRight(row1, col1, row2, col2) {
    this.#grid[parseInt(row2)][parseInt(col2)] *= 2;
    this.#score += this.#grid[parseInt(row2)][parseInt(col2)];
    this.#grid[parseInt(row1)][parseInt(col1)] = 0;
  }

  checkGameOver() {
    for (let i = 0; i < this.#gridSize; i++) {
      for (let j = 0; j < this.#gridSize; j++) {
        if (this.#grid[parseInt(i)][parseInt(j)] === 0) {
          return false; // Найдены пустые ячейки, игра не окончена
        }
        if (
          j < this.#gridSize - 1 &&
          this.#grid[parseInt(i)][parseInt(j)] === this.#grid[parseInt(i)][parseInt(j + 1)]
        ) {
          return false; // Можно объединить соседние блоки по горизонтали
        }
        if (
          i < this.#gridSize - 1 &&
          this.#grid[parseInt(i)][parseInt(j)] === this.#grid[parseInt(i + 1)][parseInt(j)]
        ) {
          return false; // Можно объединить соседние блоки по вертикали
        }
      }
    }
    return true; // Нельзя сделать дополнительных ходов, игра окончена
  }

  endGame() {
    this.#isGameOver = true;
    const gameOverText = document.getElementById('game-over-message');
    gameOverText.style.display = 'block';
    const resumeButton = document.getElementById('resume-button');
    resumeButton.style.display = 'block';
  }

  resumeGame() {
    if (this.#isGameOver) {
      this.#isGameOver = false;
      const resumeButton = document.getElementById('resume-button');
      resumeButton.style.display = 'none';
      const gameOverText = document.getElementById('game-over-message');
      gameOverText.style.display = 'none';
      this.initializeGame();
    }
  }

  showBonusMessage() {
    this.bonusMessageElement.style.display = 'block';
    setTimeout(() => {
      this.bonusMessageElement.style.display = 'none';
    }, 1000);
  }

  duplicateTiles() {
    for (let i = 0; i < this.#gridSize; i++) {
      for (let j = 0; j < this.#gridSize; j++) {
        if (this.#grid[parseInt(i)][parseInt(j)] > 0) {
          this.#grid[parseInt(i)][parseInt(j)] *= 2;
        }
      }
    }
    this.updateGridDisplay();
  }

  addRandomTile() {
    const availableCells = [];
    for (let i = 0; i < this.#gridSize; i++) {
      for (let j = 0; j < this.#gridSize; j++) {
        if (this.#grid[parseInt(i)][parseInt(j)] === 0) {
          availableCells.push({ row: i, col: j });
        }
      }
    }

    if (availableCells.length > 0) {
      const maxRandomValue = 4.294967295e9;
      const randomValue = window.crypto.getRandomValues(new Uint32Array(1))[0] / maxRandomValue;
      const randomIndex = Math.floor(randomValue * availableCells.length);

      if (randomIndex >= 0 && randomIndex < availableCells.length) {
        const randomCell = availableCells[parseInt(randomIndex)];
        this.#grid[parseInt(randomCell.row)][parseInt(randomCell.col)] = randomValue < 0.9 ? 2 : 4;
      }
    }
    this.updateGridDisplay();
  }

  moveBlockLeft(fromRow, fromCol, toRow, toCol) {
    this.#grid[parseInt(toRow)][parseInt(toCol)] = this.#grid[parseInt(fromRow)][parseInt(fromCol)];
    this.#grid[parseInt(fromRow)][parseInt(fromCol)] = 0;
  }

  mergeBlocksLeft(row1, col1, row2, col2) {
    if (this.#grid[parseInt(row2)][parseInt(col2)] === 16) {
      this.#bonusActive = true;
      this.#score += 100;
      this.activateBonusLeft();
      this.showBonusMessage();
    }

    this.#grid[parseInt(row2)][parseInt(col2)] *= 2;
    this.#score += this.#grid[parseInt(row2)][parseInt(col2)];
    this.#grid[parseInt(row1)][parseInt(col1)] = 0;
  }
}

const gridContainer = document.querySelector('.grid-container');
const scoreElement = document.querySelector('.score');
const bonusMessageElement = document.querySelector('.bonus-message');
const gridSize = 4;

const game = new Game2048(gridSize, gridContainer, scoreElement, bonusMessageElement);

console.log(game);
