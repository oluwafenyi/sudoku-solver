import unittest
from assets.board import Cell, Board


class CellTests(unittest.TestCase):
    def test_cell_in_board(self):
        cell = Cell(0, 0, 5)
        board = [cell]
        self.assertTrue(Cell(0, 0) in board)

    def test_cell_equality(self):
        self.assertEqual(Cell(0, 0, 5), Cell(0, 0, 2))

    def test_cell_fixed(self):
        cell = Cell(0, 0, 5, isfixed=True)
        self.assertFalse(not cell.isfixed)


class BoardTests(unittest.TestCase):
    def test_board_iterable(self):
        board = Board(2)
        board.input_cells([])
        self.assertEqual([cell for cell in board], [Cell(0, 0, 0), Cell(0, 1, 0), Cell(1, 0, 0), Cell(1, 1, 0)])


if __name__ == "__main__":
    unittest.main()
