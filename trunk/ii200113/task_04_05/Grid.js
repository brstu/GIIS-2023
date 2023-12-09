const crypto = require("crypto");
const Grid_size = 4;
const Cell_size = 20;
const Cell_gap = 2;

function secureRandom() {
  return crypto.randomInt(100) / 1000;
}
export default class Grid {
  #cells;

  constructor(gridElement) {
    gridElement.style.setProperty("--grid-size", Grid_size);
    gridElement.style.setProperty("--cell-size", `${Cell_size}vmin`);
    gridElement.style.setProperty("--cell-gap", `${Cell_gap}vmin`);
    this.#cells = createCellElements(gridElement).map((cellElement, index) => {
      return new Cell(
        cellElement,
        index % Grid_size,
        Math.floor(index / Grid_size)
      );
    });
  }

  get cells() {
    return this.#cells;
  }

  get cellsByRow() {
    return this.#cells.reduce((cellGrid, cell) => {
      cellGrid[cell.y] = cellGrid[cell.y] || [];
      cellGrid[cell.y][cell.x] = cell;
      return cellGrid;
    }, []);
  }

  get cellsByColumn() {
    return this.#cells.reduce((cellGrid, cell) => {
      cellGrid[cell.x] = cellGrid[cell.x] || [];
      cellGrid[cell.x][cell.y] = cell;
      return cellGrid;
    }, []);
  }

  get #emptyCells() {
    return this.#cells.filter((cell) => cell.tile == null);
  }

  randomEmptyCell() {
    const randomIndex = Math.floor(secureRandom() * this.#emptyCells.length);
    return this.#emptyCells[randomIndex];
  }
}

class Cell {
  CELLELEMENT;
  Xpoint;
  Ypoint;
  #tile;
  #mergeTile;

  constructor(cellElement, x, y) {
    this.CELLELEMENT = cellElement;
    this.Xpoint = x;
    this.Ypoint = y;
  }

  get x() {
    return this.Xpoint;
  }

  get y() {
    return this.Ypoint;
  }

  get tile() {
    return this.#tile;
  }

  set tile(value) {
    this.#tile = value;
    if (value == null) return;
    this.#tile.x = this.Xpoint;
    this.#tile.y = this.Ypoint;
  }

  get mergeTile() {
    return this.#mergeTile;
  }

  set mergeTile(value) {
    this.#mergeTile = value;
    if (value == null) return;
    this.#mergeTile.x = this.Xpoint;
    this.#mergeTile.y = this.Ypoint;
  }

  canAccept(tile) {
    return (
      this.tile == null ||
      (this.mergeTile == null && this.tile.value === tile.value)
    )
  }

  mergeTiles() {
    if (this.tile == null || this.mergeTile == null) return;
    this.tile.value = this.tile.value + this.mergeTile.value;
    this.mergeTile.remove();
    this.mergeTile = null;
  }
}

function createCellElements(gridElement) {
  const cells = [];
  for (let i = 0; i < Grid_size * Grid_size; i++) {
    const cell = document.createElement("div");
    cell.classList.add("cell");
    cells.push(cell);
    gridElement.append(cell);
  }
  return cells;
}
