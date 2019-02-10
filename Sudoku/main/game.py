from main.board import Board
from main.data_manager import DataManager
from main.exceptions import ImpossibleToSolveError
from main.solver import Solver


class Game:
    def __init__(self, solve=False):
        self.solve = solve
        self.data_manager = DataManager() if solve else None
        self.data = self.data_manager.read_data() if self.data_manager else None
        self.board = Board(data=self.data)
        self.solver = Solver(self.board) if solve else None

    def run(self):
        if self.solve:
            # Solve existing SuDoKu
            self.board.display()
            input('\n<enter> to solve...\n')
            self.solve_board()
            self.board.display()
        else:
            # Generate random SuDoKu
            raise NotImplementedError

    def solve_board(self):
        try:
            while not self.solver.is_solved():
                self.solver.place_next()
        except ImpossibleToSolveError:
            print('\nThis SuDoKu is impossible to solve with any of the implemented techniques.')
            print('\nPencil marks:\n')
            self.solver.display_pencil_marks()
