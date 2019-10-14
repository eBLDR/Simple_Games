from xiangqi import constants
from xiangqi.pieces.piece import Piece


class Soldier(Piece):
    def __init__(self, starting_point):
        super().__init__(constants.SOLDIER, starting_point)
