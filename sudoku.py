
import eel

from board import Cell, Board


board = Board()
eel.init('web', allowed_extensions=('.js', '.html'))


@eel.expose
def clear_board():
    board.board = []
    board.init_board()


@eel.expose
def input_cell(x, y, value):
    cell = Cell(x, y, value)
    if value != 0:
        cell.isfixed = True
    board.input_cell(cell)

    if cell.value == 0:
        eel.setCellColor(cell.x, cell.y, 'unset')

    for c in board:
        if c.isfixed is True:
            eel.setCellColor(c.x, c.y, 'fixed')
        else:
            eel.setCellColor(c.x, c.y, 'unset')

    if not board.is_valid():
        for cell_, classes in board.errors.items():
            for c in board:
                if 'x' in classes:
                    if c.x == cell_.x and c.value == cell_.value:
                        eel.setCellColor(c.x, c.y, 'error')
                if 'y' in classes:
                    if c.y == cell_.y and c.value == cell_.value:
                        eel.setCellColor(c.x, c.y, 'error')
                if 'b' in classes:
                    if c.block == cell_.block and c.value == cell_.value:
                        eel.setCellColor(c.x, c.y, 'error')


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
    n = 0
    for m in range(9):
        if m % 3 == 0 and m > 0:
            n += 3
        seq = list(range(n, n+3))
        if m == i:
            return seq
    raise IndexError


if __name__ == '__main__':
    eel.start(
        'templates/index.html',
        jinja_templates='templates',
        size=(500,548),
        context={'generate_seq': generate_seq, 'enumerate': enumerate, 'get_col_seq': get_col_seq},
    )
