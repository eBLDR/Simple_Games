from main.board import Board
from main.data_manager import DataManager
from main.solver import Solver


class Game:
    def __init__(self, solve=False):
        self.solve = solve

        self.data_manager = DataManager() if solve else None
        self.data = self.data_manager.read_data() if self.data_manager else None
        self.board = Board(data=self.data)

    def run(self):
        if self.solve:
            self.board.solve()
        else:
            raise NotImplementedError
        self.board.display()
