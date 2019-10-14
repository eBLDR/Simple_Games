from xiangqi import constants
from xiangqi.pieces.piece import Piece


class Chariot(Piece):
    def __init__(self, starting_point):
        super().__init__(constants.CHARIOT, starting_point)
