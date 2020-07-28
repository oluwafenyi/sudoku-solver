eel = window.eel;


const board = [];

const colorConfig = {
  fixed: {
    color: 'white',
    background: 'gray'
  },
  error: {
    color: 'white',
    background: 'red'
  },
  unset: {
    color: 'gray',
    background: 'white'
  }
};


for (let y = 0; y < 9; y++) {
  const row = [];
  for (let x = 0; x < 9; x++) {
    const element = document.getElementById('cell-' + x + '-' + y);
    row.push(element);
  }
  board.push(row);
}

board.forEach(row => {
  row.forEach(cell => {
    cell.addEventListener('keydown', (e) => {
      const coords = e.srcElement.id.split('-');
      const x = Number(coords[1]);
      const y = Number(coords[2]);

      if (e.key == 'Backspace') {
        eel.input_cell(x, y, 0);
      }
      else {
        const value = Number(e.key);
        eel.input_cell(x, y, value);
      }
    });
  });
});

function clearCells() {
  board.forEach(row => {
    row.forEach(cell => {
      cell.value = '';
      cell.style['background'] = 'white';
      cell.style['color'] = 'black';
    });
  });
  eel.clear_board();
}

function solveBoard() {
  eel.solve();
}

function insertCellValue(x, y, value) {
  board[y][x].value = value.toString();
}

function setCellColor(x, y, status) {
  board[y][x].style['background'] = colorConfig[status]['background'];
  board[y][x].style['color'] = colorConfig[status]['color'];
}

eel.expose(insertCellValue);
eel.expose(setCellColor);
