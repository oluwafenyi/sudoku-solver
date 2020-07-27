
import eel

from board import Cell, Board


board = Board()
eel.init('web', allowed_extensions=('.js', '.html'))

@eel.expose
def clear_board():
    board.init_board()

@eel.expose
def input_cell(x, y, value):
    cell = Cell(x, y, value)
    if value != 0:
        cell.isfixed = True
    board.input_cell(cell)

@eel.expose
def solve():
    solved_board = Board.solve(board)
    for cell in solved_board:
        if not cell.isfixed:
            eel.insertCellValue(cell.x, cell.y, cell.value)

def generate_seq():
    n = 0
    for i in range(9):
        yield list(range(n, n+3))
        n += 3
        if n == 9:
            n = 0

def get_col_seq(i):
    seqs = []
    n = 0
    for m in range(9):
        if m % 3 == 0 and m > 0:
            n += 3
        seq = list(range(n, n+3))
        seqs.append(seq)
    return seqs[i]


if __name__ == '__main__':
    eel.start(
        'templates/index.html',
        jinja_templates='templates',
        size=(500,548),
        context={'generate_seq': generate_seq, 'enumerate': enumerate, 'get_col_seq': get_col_seq}
    )
