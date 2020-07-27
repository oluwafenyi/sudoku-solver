
from board import Board, Cell


# board = [
#     [3, 9, 7, None, None, 1, None, None, None],
#     [None, None, 2, 8, None, None, None, None, 7],
#     [1, 5, 8, 7, 2, 9, None, 3, 6],
#     [8, None, None, None, None, 2, None, 4, None],
#     [None, 3, 5, 4, 1, 7, 8, None, None],
#     [None, 4, 1, None, None, 6, None, 5, 2],
#     [None, None, None, None, None, 3, None, 1, None],
#     [None, None, None, 1, 9, 8, 5, None, None],
#     [7, 1, None, 5, None, None, None, None, None]
# ]

board = [
    [None, None, None, None, 3, None, None, None, None],
    [None, 1, 3, 4, None, 8, 9, None, None],
    [None, 9, None, 5, None, None, None, 8, None],
    [4, None, None, None, 9, None, 2, None, 5],
    [None, 5, 2, None, None, 1, None, None, 7],
    [6, None, None, 2, None, 5, 4, None, None],
    [3, None, None, 6, None, 4, 5, None, None],
    [None, 2, 7, None, None, None, 6, None, 9],
    [None, 4, 6, None, None, 9, None, None, None]
]

sudoku_board = Board()

for x, row in enumerate(board):
    for y, cell in enumerate(row):
        value = cell if cell is not None else 0
        cell = Cell(x, y, val=value)
        sudoku_board.input_cell(cell)

if sudoku_board.is_valid():
    solved = Board.solve(sudoku_board)
    for cell in solved:
        print(cell.value)
else:
    print('invalid board')
