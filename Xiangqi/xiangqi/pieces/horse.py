from xiangqi import constants
from xiangqi.pieces.piece import Piece


class Horse(Piece):
    def __init__(self, starting_point):
        super().__init__(constants.HORSE, starting_point)
