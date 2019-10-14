from xiangqi import constants


class Piece:
    def __init__(self, name, starting_point):
        self.name = name
        self.starting_point = starting_point
        self.point = self.starting_point

    def __repr__(self):
        return constants.PIECES_REFERENCE[self.name]

    def get_rank_and_file(self):
        return int(self.point[0]), int(self.point[1])

    def move(self, new_point):
        self.point = new_point
