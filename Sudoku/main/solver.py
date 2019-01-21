from main.exceptions import ImpossibleToSolveError


class Solver:
    def __init__(self, board):
        """
        The brain.
        :param board: Board instance with data.
        """
        self.board = board

    def is_solved(self):
        return all([all(row) for row in self.board.board])

    @staticmethod
    def display_info(new_number, row_index, column_index, method):
        print('Placed number {} at row:column {}:{} by {}.'.format(new_number, row_index + 1, column_index + 1, method))

    def get_possible_numbers(self):
        return [str(n) for n in range(1, self.board.size + 1)]

    def get_row_indexes(self, row_index):
        return [(row_index, column_index) for column_index in range(self.board.size)]

    def get_column_indexes(self, column_index):
        return [(row_index, column_index) for row_index in range(self.board.size)]

    def get_square_indexes(self, row_index, column_index):
        row_start_index = (row_index // self.board.dimension) * self.board.dimension
        row_range = range(row_start_index, row_start_index + self.board.dimension)
        column_start_index = (column_index // self.board.dimension) * self.board.dimension
        column_range = range(column_start_index, column_start_index + self.board.dimension)
        return [(row_index, column_index) for row_index in row_range for column_index in column_range]

    def get_values(self, indexes):
        return [self.board.board[row][column] for row, column in indexes]

    def get_row_values(self, row_index):
        return self.get_values(self.get_row_indexes(row_index))

    def get_column_values(self, column_index):
        return self.get_values(self.get_column_indexes(column_index))

    def get_square_values(self, row_index, column_index):
        return self.get_values(self.get_square_indexes(row_index, column_index))

    def update_board(self, new_number, row_index, column_index, method):
        self.board.board[row_index][column_index] = new_number
        self.display_info(new_number, row_index, column_index, method)

    def place_next(self):
        """
        Main logic of techniques usage.
        :return: True if successful match False otherwise.
        """
        if self.place_by_number_elimination():
            return
        if self.place_by_single_position():
            return
        raise ImpossibleToSolveError

    def place_by_number_elimination(self):
        """
        Tries to place a number based on number elimination, checking rows, columns and squares.
        """

        def remove_matches(list_):
            for number in list_:
                if number in possible_matches:
                    possible_matches.remove(number)

        for row_index in range(self.board.size):
            for column_index in range(self.board.size):
                if self.board.board[row_index][column_index]:
                    # Skip if there is already a number
                    continue

                possible_matches = self.get_possible_numbers()

                # Row check
                remove_matches(self.get_row_values(row_index))

                # Column check
                remove_matches(self.get_column_values(column_index))

                # Square check
                remove_matches(self.get_square_values(row_index, column_index))

                # Place number if there is only one match left
                if len(possible_matches) == 1:
                    self.update_board(possible_matches[0], row_index, column_index, 'number elimination')
                    return True

        return False

    def place_by_single_position(self):
        """
        Tries to place a number based on single position possible.
        """
        for number in self.get_possible_numbers():
            # Single position in square
            for row_index in range(0, self.board.size, self.board.dimension):
                for column_index in range(0, self.board.size, self.board.dimension):
                    if number in self.get_square_values(row_index, column_index):
                        # Skip if the number is already in that square
                        continue
                    possible_coordinates = [indexes for indexes in self.get_square_indexes(row_index, column_index) if not self.board.board[indexes[0]][indexes[1]]]
                    for row, column in possible_coordinates.copy():
                        if number in self.get_row_values(row) or number in self.get_column_values(column):
                            possible_coordinates.remove((row, column))

                    if len(possible_coordinates) == 1:
                        new_row_index, new_column_index = possible_coordinates[0]
                        self.update_board(number, new_row_index, new_column_index, 'single position in square')
                        return True

            # Single position in row
            for row_index in range(self.board.size):
                if number in self.get_row_values(row_index):
                    # Skip if the number is already in that row
                    continue
                possible_coordinates = [indexes for indexes in self.get_row_indexes(row_index) if not self.board.board[indexes[0]][indexes[1]]]
                for row, column in possible_coordinates.copy():
                    if number in self.get_column_values(column):
                        possible_coordinates.remove((row, column))

                if len(possible_coordinates) == 1:
                    new_row_index, new_column_index = possible_coordinates[0]
                    self.update_board(number, new_row_index, new_column_index, 'single position in row')
                    return True

            # Single position in column
            for column_index in range(self.board.size):
                if number in self.get_column_values(column_index):
                    # Skip if the number is already in that column
                    continue
                possible_coordinates = [indexes for indexes in self.get_column_indexes(column_index) if not self.board.board[indexes[0]][indexes[1]]]
                for row, column in possible_coordinates.copy():
                    if number in self.get_row_values(row):
                        possible_coordinates.remove((row, column))

                if len(possible_coordinates) == 1:
                    new_row_index, new_column_index = possible_coordinates[0]
                    self.update_board(number, new_row_index, new_column_index, 'single position in column')
                    return True

        return False
