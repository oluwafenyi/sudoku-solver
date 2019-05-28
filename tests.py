import unittest
from sudoku import Cell


class CellTests(unittest.TestCase):
    def test_cell_in_board(self):
        cell = Cell(0, 0, 5)
        board = [cell]
        self.assertTrue(Cell(0, 0) in board)

    def test_cell_equality(self):
        self.assertEqual(Cell(0, 0, 5), Cell(0, 0, 2))


if __name__ == "__main__":
    unittest.main()
