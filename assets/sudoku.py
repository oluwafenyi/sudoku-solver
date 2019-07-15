import sys
import random

from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from SudokuGUI import Ui_MainWindow

from board import Board, Cell


class GUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.board = Board()
        self.cells = []

        self.show()
        self.ui.tableWidget.itemChanged.connect(self.on_change)
        self.ui.solveButton.clicked.connect(self.solve)


    def setCell(self, x, y, val):
        item = QTableWidgetItem(str(val))
        item.setTextAlignment(Qt.AlignCenter)
        self.ui.tableWidget.setItem(x, y, item)


    def on_change(self, item):

        if self.ui.solveButton.isEnabled():
            try:
                if item.text() == "":
                    new_cell = Cell(item.row(), item.column(),
                                    val=0, isfixed=True)
                    item.setBackground(QtGui.QColor("#ffffff"))
                elif item.text() == "0":
                    # users shouldn't enter zero as a cell value as it is already
                    # the default value.
                    raise ValueError("cannot input 0 as cell value")
                else:
                    new_cell = Cell(item.row(), item.column(),
                                    val=int(item.text()), isfixed=True)
                    item.setBackground(QtGui.QColor('#85888c'))

                # we want to avoid having a cell with val 0 self.cells
                if new_cell not in self.cells and new_cell.value != 0:
                    self.cells.append(new_cell)
                else:
                    self.cells.remove(new_cell)
                    if new_cell.value != 0:
                        self.cells.append(new_cell)

                self.board.input_cells(self.cells)
                # print(self.board)

            except ValueError:
                item.setText("")
                item.setBackground(QtGui.QColor("#ffffff"))

    def solve(self):
        self.ui.solveButton.setDisabled(True)
        self.ui.tableWidget.setDisabled(True)
        while not self.board.is_solved():
            for cell in self.board.board:
                print(cell)
                if not cell.isfixed:
                    if cell.value == 0:
                        taken_x = [c.value for c in self.board if c.value != 0 and c.x == cell.x]
                        taken_y = [c.value for c in self.board if c.value != 0 and c.y == cell.y]
                        taken_b = [c.value for c in self.board if c.value != 0 and c.block == cell.block]
                        taken_set = set(taken_x + taken_y + taken_b)
                        possible_solutions = list({i for i in range(1, self.board.dimension + 1)} - taken_set)
                        print(possible_solutions)
                        if len(possible_solutions) > 1 or len(possible_solutions) == 0:
                            continue
                        cell.value = random.choice(possible_solutions)
                        cell.possible_solutions = possible_solutions
                        self.setCell(cell.x, cell.y, cell.value)

                # elif cell.value:
                #     cell.value = random.choice(cell.possible_solutions)
                #     self.setCell(cell.x, cell.y, cell.value)

        self.ui.solveButton.setDisabled(False)
        self.ui.tableWidget.setDisabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = GUI()
    w.show()
    sys.exit(app.exec_())
