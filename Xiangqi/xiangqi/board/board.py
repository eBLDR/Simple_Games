from xiangqi import constants
from xiangqi.board.point import Point


class Board:
    def __init__(self):
        self.board = self.create_board()

    @staticmethod
    def create_board():
        board = [
            [Point(rank, file) for file in constants.FILES_RANGE]
            for rank in constants.RANK_RANGE
        ]

        return board

    def set_up_new_game(self, pieces_set):
        for piece in pieces_set:
            piece_rank, piece_file = piece.get_rank_and_file()

            for rank in self.board:
                for point in rank:
                    if point.rank == piece_rank and point.file == piece_file:
                        point.piece = piece

    def get_board_str(self):
        left_margin = ' ' * 3
        separation_bar = left_margin + '-' * constants.FILES * 3 + '--\n'
        board_str = separation_bar

        for rank, rank_coord in zip(self.board, constants.RANK_RANGE):
            board_str += '{:2} | '.format(rank_coord)

            for point, file_coord in zip(rank, constants.FILES_RANGE):
                # Add piece to line
                board_str += str(point)

                if file_coord > min(constants.FILES_RANGE):
                    board_str += '-' * 2
                else:
                    board_str += ' '

            board_str += '|\n'
            if rank_coord == 6:
                board_str += left_margin + '|' + ' ' * (
                        len(separation_bar) - len(left_margin) - 3
                ) + '|\n'

            elif rank_coord > min(constants.RANK_RANGE):
                board_str += left_margin + '| ' + '|  ' * (
                        constants.FILES - 1
                ) + '| |\n'

        # Add line coordinates
        board_str += separation_bar + ' ' * 5
        for file_coord in constants.FILES_RANGE:
            board_str += '{}  '.format(file_coord)

        return board_str
