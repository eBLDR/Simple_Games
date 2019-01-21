class Board:
    def __init__(self, size=9, data=None):
        assert size ** (1 / 2) // 1 == size ** (1 / 2) / 1, 'Invalid size - must be the square of a natural number.'

        self.size = size
        self.dimension = round(self.size ** (1 / 2))
        self.board = data if data else self.generate_empty_board()

    def generate_empty_board(self):
        return [['0'] * self.size] * self.size

    def display(self):
        board_str = ''
        separator_mapper = {'horizontal': {'thin': ' ',
                                           'thick': '='},
                            'vertical': {'thin': '   ',
                                         'thick': ' | '}}
        for row in range(len(self.board)):
            horizontal_sep_char = separator_mapper['horizontal']['thick'] if row % self.dimension == 0 else separator_mapper['horizontal']['thin']
            if row != 0:
                board_str += '\n' + separator_mapper['vertical']['thick'][:-1] + (horizontal_sep_char * (self.dimension * (len(separator_mapper['vertical']['thick']) + 1) - 1) + separator_mapper['vertical']['thick'][1:-1]) * self.dimension + '\n'
            else:
                board_str += '\n' + separator_mapper['vertical']['thick'][:-1] + separator_mapper['horizontal']['thick'] * (self.size * (len(separator_mapper['vertical']['thick']) + 1) - 1) + separator_mapper['vertical']['thick'][1:] + '\n'
            for column in range(len(self.board[row])):
                vertical_sep_char = separator_mapper['vertical']['thick'] if column % self.dimension == 0 else separator_mapper['vertical']['thin']
                board_str += vertical_sep_char + (self.board[row][column] if self.board[row][column] else ' ')
            board_str += separator_mapper['vertical']['thick']
        board_str += '\n' + separator_mapper['vertical']['thick'][:-1] + separator_mapper['horizontal']['thick'] * (self.size * (len(separator_mapper['vertical']['thick']) + 1) - 1) + separator_mapper['vertical']['thick'][1:] + '\n'
        print(board_str)
