

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

    def __key(self) -> tuple:
        return self.x, self.y

    def __repr__(self):
        return "{0.__class__.__name__}({0.x!r}, {0.y!r})".format(self)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        raise NotImplementedError

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
        self.init_board()

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

    def copy(self):
        copy = Board(dimension=self.dimension)
        copy.board = [Cell(cell.x, cell.y, cell.value, isfixed=cell.isfixed) for cell in self.board]
        return copy

    def init_board(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.board.append(Cell(i, j, val=0))


    def input_cell(self, cell: Cell):
        if cell in self.board:
            index = self.board.index(cell)
            self.board[index] = cell
        else:
            raise ValueError

    def generate_board(self, difficulty=0):
        # todo: create function to generate random valid boards
        pass

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

    def is_valid(self):
        valid = True
        region = Region(self.board)
        horizontals = region.horizontal_regions()
        verticals = region.vertical_regions()
        blocks = region.block_regions()
        self.errors = {}
        for cell in self:
            if cell.value:
                if [c.value for c in horizontals[cell.x]].count(cell.value) > 1:
                    self.errors.setdefault(cell, [])
                    self.errors[cell].append('x')
                    valid = False
                    break
                if [c.value for c in verticals[cell.y]].count(cell.value) > 1:
                    self.errors.setdefault(cell, [])
                    self.errors[cell].append('y')
                    valid = False
                    break

                if [c.value for c in self.board if c.block == cell.block].count(cell.value) > 1:
                    self.errors.setdefault(cell, [])
                    self.errors[cell].append('b')
                    valid = False
                    break
        return valid

    @staticmethod
    def solve(board):
        if board.is_solved():
            return board
        possible_solutions_set = {}
        least_possible_solutions = None
        tracked_cell = None
        for cell in board:
            if cell.isfixed:
                continue
            if cell.value == 0:
                taken_x = [c.value for c in board if c.value != 0 and c.x == cell.x]
                taken_y = [c.value for c in board if c.value != 0 and c.y == cell.y]
                taken_b = [c.value for c in board if c.value != 0 and c.block == cell.block]
                taken_set = set(taken_x + taken_y + taken_b)
                possible_solutions = list({i for i in range(1, board.dimension + 1)} - taken_set)
                if len(possible_solutions) == 1:
                    cell.value = possible_solutions[0]
                else:
                    possible_solutions_set[cell] = possible_solutions

        if [] in possible_solutions_set.values():
            return
        if not possible_solutions_set:
            return board
        sorted_set = list(sorted(possible_solutions_set.items(), key=lambda sol: len(sol[1])))
        for cell, solution_set in sorted_set:
            for solution in solution_set:
                board_copy = board.copy()
                cell_copy = Cell(cell.x, cell.y, solution)
                board_copy.input_cell(cell_copy)
                if not board_copy.is_valid():
                    continue
                solved = Board.solve(board_copy)
                if solved is not None:
                    return solved
