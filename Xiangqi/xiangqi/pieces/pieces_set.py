from xiangqi import constants
from xiangqi.pieces import Advisor, Cannon, Chariot, Elephant, General, Horse, Soldier


class PiecesSet:
    class_mapper = {
        constants.ADVISOR: Advisor,
        constants.CANNON: Cannon,
        constants.CHARIOT: Chariot,
        constants.ELEPHANT: Elephant,
        constants.GENERAL: General,
        constants.HORSE: Horse,
        constants.SOLDIER: Soldier
    }

    def __init__(self):
        self.pieces = []
        self.generate_pieces()

    def generate_pieces(self):
        for name, class_ in self.class_mapper.items():
            for point in constants.PIECES_STARTING_POINTS[name]:
                self.pieces.append(
                    class_(point)
                )
