from xiangqi.board.board import Board
from xiangqi.pieces.pieces_set import PiecesSet


class Game:
    def __init__(self):
        self.board = Board()
        self.pieces = PiecesSet()
        self.players = []

    def new_game(self):
        self.board.set_up_new_game(
            self.pieces.pieces
        )

    def run(self):
        self.new_game()
        print(self.board.get_board_str())
