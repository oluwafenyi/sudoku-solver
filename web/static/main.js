eel = window.eel;


const board = [];

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
    cell.addEventListener('change', (e) => {
      if (e.target.value.trim() == '') {
        e.srcElement.style['background'] = 'white';
        e.srcElement.style['color'] = 'black';
      }
      else {
        e.srcElement.style['background'] = 'gray';
        e.srcElement.style['color'] = 'white';
        const coords = e.srcElement.id.split('-');
        const x = Number(coords[1]);
        const y = Number(coords[2])
        const value = Number(e.target.value);
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

eel.expose(insertCellValue)
