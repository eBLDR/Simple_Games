from xiangqi import constants
from xiangqi.pieces.piece import Piece


class Elephant(Piece):
    def __init__(self, starting_point):
        super().__init__(constants.ELEPHANT, starting_point)
