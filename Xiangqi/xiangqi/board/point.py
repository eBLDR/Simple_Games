class Point:
    def __init__(self, rank, file):
        self.rank = rank
        self.file = file
        self.piece = None

    def __repr__(self):
        return str(self.piece) if self.piece else '-'

    def add_piece(self, piece):
        self.piece = piece

    def remove_piece(self):
        self.piece = None
