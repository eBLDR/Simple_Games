from main.exceptions import ImpossibleToSolveError


class Solver:
    def __init__(self, board):
        """
        The brain.
        :param board: Board instance with data.
        """
        self.board = board
        self.pencil_marks = {}
        self.initialise_pencil_marks()

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

    def get_block_indexes(self, row_index, column_index):
        row_start_index = (row_index // self.board.dimension) * self.board.dimension
        row_range = range(row_start_index, row_start_index + self.board.dimension)
        column_start_index = (column_index // self.board.dimension) * self.board.dimension
        column_range = range(column_start_index, column_start_index + self.board.dimension)
        return [(row_index, column_index) for row_index in row_range for column_index in column_range]

    def _get_values(self, indexes):
        return [self.board.board[row][column] for row, column in indexes]

    def get_row_values(self, row_index):
        return self._get_values(self.get_row_indexes(row_index))

    def get_column_values(self, column_index):
        return self._get_values(self.get_column_indexes(column_index))

    def get_block_values(self, row_index, column_index):
        return self._get_values(self.get_block_indexes(row_index, column_index))

    def get_row_pencil_marks(self, row_index):
        return {key: self.pencil_marks[key] for key in self.get_row_indexes(row_index) if key in self.pencil_marks.keys()}

    def get_column_pencil_marks(self, column_index):
        return {key: self.pencil_marks[key] for key in self.get_column_indexes(column_index) if key in self.pencil_marks.keys()}

    def get_block_pencil_marks(self, row_index, column_index):
        return {key: self.pencil_marks[key] for key in self.get_block_indexes(row_index, column_index) if key in self.pencil_marks.keys()}

    def initialise_pencil_marks(self):
        """
        Populates pencil marks dictionary with possible matches by position.
        """

        def remove_matches(list_):
            for number in list_:
                if number in possible_matches:
                    possible_matches.remove(number)

        for row_index in range(self.board.size):
            for column_index in range(self.board.size):
                if self.board.board[row_index][column_index]:
                    # Skip if there is already a number in that cell
                    continue

                possible_matches = self.get_possible_numbers()

                # Block check
                remove_matches(self.get_block_values(row_index, column_index))

                # Row check
                remove_matches(self.get_row_values(row_index))

                # Column check
                remove_matches(self.get_column_values(column_index))

                self.pencil_marks[(row_index, column_index)] = possible_matches

    def display_pencil_marks(self):
        for index in sorted(self.pencil_marks.keys()):
            if len(self.pencil_marks[index]) == 3:
                print('{}: {}'.format(index, ', '.join(self.pencil_marks[index])))

    def _update_board(self, new_number, row_index, column_index, method):
        """
        Places the new number into the existing board.
        """
        self.board.board[row_index][column_index] = new_number
        self.display_info(new_number, row_index, column_index, method)

    def _update_pencil_marks(self, new_number, row_index, column_index):
        """
        Updates the pencil marks candidates based on the new number placed.
        """

        def remove_candidates(key, number, pencil_marks):
            if key in pencil_marks.keys() and number in pencil_marks[key]:
                pencil_marks[key].remove(number)

        # Block update
        for index in self.get_block_indexes(row_index, column_index):
            remove_candidates(index, new_number, self.pencil_marks)

        # Row update
        for index in self.get_row_indexes(row_index):
            remove_candidates(index, new_number, self.pencil_marks)

        # Column update
        for index in self.get_column_indexes(column_index):
            remove_candidates(index, new_number, self.pencil_marks)

        del self.pencil_marks[(row_index, column_index)]

    def update(self, new_number, row_index, column_index, method):
        """
        Updates the board and the pencil marks.
        :param new_number: number
        :param row_index: row
        :param column_index: column
        :param method: technique used to place the number
        """
        self._update_board(new_number, row_index, column_index, method)
        self._update_pencil_marks(new_number, row_index, column_index)

    def place_next(self):
        """
        Main logic of techniques usage.
        :return: True if successful placing False otherwise.
        """
        if self.lone_singles():
            return
        if self.hidden_singles():
            return
        if self.naked_pairs():
            return
        if self.omission():
            return
        raise ImpossibleToSolveError

    def lone_singles(self):
        """
        Searches for a lone single, a sole candidate in a cell.
        """
        for indexes, possible_matches in self.pencil_marks.items():
            if len(possible_matches) == 1:
                self.update(possible_matches[0], indexes[0], indexes[1], 'lone single')
                return True

        return False

    def hidden_singles(self):
        """
        Searches for a hidden single, a unique possible position left in a given house.
        """

        def find_match(house_pencil_marks):
            for candidate_number in self.get_possible_numbers():
                matches = 0
                candidate_position = None
                for indexes, candidates in house_pencil_marks.items():
                    if candidate_number in candidates:
                        matches += 1
                        if not candidate_position:
                            candidate_position = indexes
                if matches == 1:
                    return candidate_number, candidate_position
            return None, None

        # Hidden singles in block
        for row_index in range(0, self.board.size, self.board.dimension):
            for column_index in range(0, self.board.size, self.board.dimension):
                number, position = find_match(self.get_block_pencil_marks(row_index, column_index))
                if number and position:
                    self.update(number, position[0], position[1], 'hidden single in block')
                    return True

        # Hidden singles in row
        for row_index in range(self.board.size):
            number, position = find_match(self.get_row_pencil_marks(row_index))
            if number and position:
                self.update(number, position[0], position[1], 'hidden single in row')
                return True

        # Hidden singles in column
        for column_index in range(self.board.size):
            number, position = find_match(self.get_row_pencil_marks(column_index))
            if number and position:
                self.update(number, position[0], position[1], 'hidden single in column')
                return True

        return False

    def naked_pairs(self):
        """
        Clears pencil marks based on equivalent candidates in two cells.
        """

        def find_match(house_pencil_marks):
            match_ = False
            for indexes_1, candidates_1 in house_pencil_marks.items():
                if len(candidates_1) == 2:
                    for indexes_2, candidates_2 in house_pencil_marks.items():
                        if len(candidates_2) == 2 and indexes_1 != indexes_2 and candidates_1 == candidates_2:

                            for index in house_pencil_marks.keys():
                                if index != indexes_1 and index != indexes_2:
                                    for candidate in candidates_1:
                                        if candidate in self.pencil_marks[index]:
                                            self.pencil_marks[index].remove(candidate)
                                            match_ = True

            return match_

        match = False

        # Naked pairs in block
        for row_index in range(0, self.board.size, self.board.dimension):
            for column_index in range(0, self.board.size, self.board.dimension):
                if find_match(self.get_block_pencil_marks(row_index, column_index)):
                    match = True
                    print('Naked pair found in block.')

        # Naked pairs in row
        for row_index in range(self.board.size):
            if find_match(self.get_row_pencil_marks(row_index)):
                match = True
                print('Naked pair found in row.')

        # Naked pairs in column
        for column_index in range(self.board.size):
            if find_match(self.get_row_pencil_marks(column_index)):
                match = True
                print('Naked pair found in column.')

        return match

    def omission(self):
        """
        Clears pencil marks by omission.
        """

        def find_match(house_pencil_marks_1, house_pencil_marks_2):
            for number in self.get_possible_numbers():
                possible_match = False
                match_ = False
                for indexes, candidates in house_pencil_marks_1.items():
                    if number in candidates and indexes in house_pencil_marks_2.keys():
                        possible_match = True
                    elif number in candidates and indexes not in house_pencil_marks_2.keys():
                        possible_match = False
                        break

                if possible_match:
                    for indexes, candidates in house_pencil_marks_2.items():
                        if number in candidates and indexes not in house_pencil_marks_1.keys():
                            self.pencil_marks[indexes].remove(number)
                            match_ = True

                return match_

        match = False

        # Row-block match
        for row_index in range(self.board.size):
            row_pencil_marks = self.get_row_pencil_marks(row_index)
            for column_index in range(0, self.board.size, self.board.dimension):
                block_pencil_marks = self.get_block_pencil_marks(row_index, column_index)
                if find_match(row_pencil_marks, block_pencil_marks) or find_match(block_pencil_marks, row_pencil_marks):
                    match = True
                    print('Omission found in row-block.')

        # Column-block match
        for column_index in range(self.board.size):
            column_pencil_marks = self.get_column_pencil_marks(column_index)
            for row_index in range(0, self.board.size, self.board.dimension):
                block_pencil_marks = self.get_block_pencil_marks(column_index, row_index)
                if find_match(column_pencil_marks, block_pencil_marks) or find_match(block_pencil_marks, column_pencil_marks):
                    match = True
                    print('Omission found in column-block.')

        return match
