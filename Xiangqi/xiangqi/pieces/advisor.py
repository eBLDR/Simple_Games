from xiangqi import constants
from xiangqi.pieces.piece import Piece


class Advisor(Piece):
    def __init__(self, starting_point):
        super().__init__(constants.ADVISOR, starting_point)
