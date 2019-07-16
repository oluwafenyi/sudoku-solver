

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
        return "{0.__class__.__name__}({0.x!r}, {0.y!r})".format(self)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def value(self):
        return self.val

    @value.setter
    def value(self, val):
        if not self.isfixed:
            self.val = val
        else:
            raise TypeError("fixed cells do not support item assignment")

    @property
    def block(self):
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
                if cell.x == i:
                    buffer.append(cell)
            if buffer:
                horizontals.append(buffer)

        return horizontals

    def vertical_regions(self):
        horizontals = self.horizontal_regions()
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
                    if cell.block == (i, j):
                        buffer.append(cell)
                if buffer:
                    blocks.append(buffer)

        return blocks

    def is_valid(self, array):
        buffer = []
        for cell in array:
            if cell.value not in buffer:
                buffer.append(cell.value)
        return len(buffer) == self.board_dimension and 0 not in buffer


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

    def __getitem__(self, i):
        if i < len(self.board):
            return self.board[i]
        else:
            raise IndexError("index out of range")

    def input_cells(self, cells: list):
        """
        takes in a list of cells and fills the gap with zero-cells
        """
        buffer = []
        for i in range(self.dimension):
            for j in range(self.dimension):
                if Cell(i, j) not in cells:
                    buffer.append(Cell(i, j, 0))

        buffer += cells
        self.board = sorted(buffer, key=lambda cell: (cell.x, cell.y))

    def generate_board(self, difficulty=0):
        # todo: create function to generate random boards
        pass

    @property
    def is_solved(self):
        solved = True
        region = Region(self.board)
        horizontals = region.horizontal_regions()
        verticals = region.vertical_regions()
        blocks = region.block_regions()

        for i in range(self.dimension):

            if not region.is_valid(horizontals[i]):
                solved = False
                break

            if not region.is_valid(verticals[i]):
                solved = False
                break

            if not region.is_valid(blocks[i]):
                solved = False
                break

        return solved

    @property
    def is_valid(self):
        valid = True
        region = Region(self.board)
        horizontals = region.horizontal_regions()
        verticals = region.vertical_regions()
        blocks = region.block_regions()
        for cell in self.board:
            if cell.value:
                if [c.value for c in horizontals[cell.x]].count(cell.value) > 1:
                    valid = False
                    break
                if [c.value for c in verticals[cell.y]].count(cell.value) > 1:
                    valid = False
                    break

                if [c.value for c in self.board if c.block == cell.block].count(cell.value) > 1:
                    valid = False
                    break
        return valid