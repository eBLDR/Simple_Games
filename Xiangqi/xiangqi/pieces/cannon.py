from xiangqi import constants
from xiangqi.pieces.piece import Piece


class Cannon(Piece):
    def __init__(self, starting_point):
        super().__init__(constants.CANNON, starting_point)
