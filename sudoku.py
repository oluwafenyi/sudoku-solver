import sys
import random
from PyQt5.QtWidgets import QMainWindow, QApplication
from SudokuGUI import Ui_MainWindow


class Cell:
    def __init__(self, x, y, val=0, grid_dimension=9, isfixed=False):
        if not isinstance(val, int):
            raise TypeError("value in cell must be an int")

        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("cell coordinates must be an int")

        if val > grid_dimension:
            raise ValueError("value is invalid for this board dimension")

        if val < 0:
            raise ValueError("value can not be negative")

        self.x = x
        self.y = y
        self.val = val
        self.isfixed = isfixed
        self.grid_dimension = grid_dimension

    def __repr__(self):
        # return "{0.__class__.__name__}({0.x!r}, {0.y!r})".format(self)
        return repr(self.val)

    def __eq__(self, other):
        return (self.x == other.row) and (self.y == other.column)

    def __ne__(self, other):
        return not self.__eq__(other)

    def is_filled(self):
        return bool(self.val)

    @property
    def row(self):
        return self.x

    @property
    def column(self):
        return self.y

    @property
    def value(self):
        return self.val

    @value.setter
    def value(self, val):
        if not self.isfixed:
            self.val = val
        else:
            raise TypeError("fixed cells do not support item assignment")

    def block_position(self):
        sqrt = int(self.grid_dimension**0.5)
        buffer = [i for i in range(sqrt) for j in range(sqrt)]
        return buffer[self.x], buffer[self.y]


class Region:
    def __init__(self, board):
        self.board = board
        self.board_dimension = int(len(self.board) ** 0.5)

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(Board(len(self.board)**2))})"

    def horizontal_regions(self):
        horizontals = []
        for i in range(self.board_dimension):
            buffer = []
            for cell in self.board:
                if cell.row == i:
                    buffer.append(cell)
            if buffer:
                horizontals.append(buffer)

        return horizontals

    def vertical_regions(self):
        horizontals = self._horizontal_regions()
        verticals = []
        for i in range(len(horizontals)):
            buffer = []
            for row in horizontals:
                buffer.append(row[i])
            verticals.append(buffer)

        return verticals

    def block_regions(self):
        blocks = []
        for i in range(self.board_dimension):
            for j in range(self.board_dimension):
                buffer = []
                for cell in self.board:
                    if cell.block_position() == (i, j):
                        buffer.append(cell)
                if buffer:
                    blocks.append(buffer)

        return blocks

    def isvalid(self, array):
        buffer = []
        for cell in array:
            if cell.value not in buffer:
                buffer.append(cell.value)
        return len(buffer) == self.board_dimension


class Board:
    def __init__(self, dimension=9):
        self.dimension = dimension
        self.board = []

    def __repr__(self):
        return "{0.__class__.__name__}({0.dimension!r})".format(self)

    def __str__(self):
        string = "{0.dimension} X {0.dimension} Sudoku Board".format(self)
        if self.board:
            string = str(self.board)
        return string

    def __iter__(self):
        self.itercounter = 0
        return self

    def __next__(self):
        if self.itercounter < len(self.board):
            cell = self.board[self.itercounter]
            self.itercounter += 1
            return cell
        raise StopIteration()

    def input_board(self, board):
        for i in range(self.dimension):
            for j in range(self.dimension):
                if Cell(i, j) not in board:
                    board.append(Cell(i, j, 0))

        self.board = sorted(board, key=lambda cell: (cell.row, cell.column))

    def generate_board(self, difficulty=0):
        # TODO: Make function have more cells that aren't filled based on
        # difficulty
        for row in range(self.dimension):
            for col in range(self.dimension):
                self.board.append(Cell(row, col, val=random.randint(0, 9)))

    def board_is_solved(self):
        is_solved = 1
        region = Region(self.board)
        for i in range(self.dimension):
            if not region.isvalid(region.horizontal_regions()[i]):
                is_solved *= 0
                break

            if not region.isvalid(region.vertical_regions()[i]):
                is_solved *= 0
                break

            if not region.isvalid(region.block_regions()[i]):
                is_solved *= 0
                break

        return is_solved == 1

    def solve_board(self):
        while not self.board_is_solved():
            pass


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.board = Board()
        self.cells = []

        self.show()
        self.ui.tableWidget.itemChanged.connect(self.on_change)

    def on_change(self, item):
        try:
            if item.text() == "":
                new_cell = Cell(item.row(), item.column(),
                                val=0, isfixed=True)
            elif item.text() == "0":
                # users shouldn't enter zero as a cell value as it is already
                # the default value.
                raise ValueError("cannot input 0 as valid cell value")
            else:
                new_cell = Cell(item.row(), item.column(),
                                val=int(item.text()), isfixed=True)

            # we want to avoid having a cell with val 0 self.cells
            if new_cell not in self.cells and new_cell.value != 0:
                self.cells.append(new_cell)
            else:
                self.cells.remove(new_cell)
                if new_cell.value != 0:
                    self.cells.append(new_cell)

            self.board.input_board(self.cells)
            # print(self.board)

        except ValueError:
            self.ui.tableWidget.item(item.row(), item.column()).setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = GUI()
    w.show()
    sys.exit(app.exec_())
