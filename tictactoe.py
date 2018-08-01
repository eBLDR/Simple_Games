# Simple Tic Tac Toe version, by BLDR.

import random
import os
import time


class Game:  # game object, keeps track of who is turn

    def __init__(self, players, board_size):
        # number of players in the game (1 for vs. AI)
        self.AI = False
        self.players = players
        if self.players == 1:
            self.AI = True

        self.history_player_1 = []
        self.history_player_2 = []

        self.current_player = random.randint(1, 2)  # who starts

        self.board = Board(board_size)  # creating and assigning board to game

    def next_player(self):
        if self.current_player == 1:
            self.current_player = 2
        elif self.current_player == 2:
            self.current_player = 1

    def get_history(self):
        if self.current_player == 1:
            return self.history_player_1
        else:
            return self.history_player_2

    def update_player_history(self, coord):
        if self.current_player == 1:
            self.history_player_1.append(coord)
        else:
            self.history_player_2.append(coord)


class Board:  # board object

    def __init__(self, n):
        self.size = n  # n x n
        # self.winning_condition = w  # required number of consecutive marks to win
        self.board = self.create_board()
        self.free_spaces = n * n
        self.winning_combination = False

    def create_board(self) -> list:
        """ Creates board n x n. """
        b = []          # empty board
        for i in range(self.size):
            r = []      # empty row
            for j in range(self.size):
                r.append(0)  # default value 0, free space
            b.append(r)
        return b

    def gen_display_str(self) -> str:
        """ Return a string ready to print. """
        output = ''
        for i in range(self.size):
            for j in range(self.size):
                char = ''
                if self.board[i][j] == 0:       # free
                    char = ' '
                elif self.board[i][j] == 1:     # player 1
                    char = 'X'
                elif self.board[i][j] == 2:     # player 2
                    char = 'O'
                output += ' ' + char + ' '
                if j != (self.size - 1):
                    output += '|'
            if i != (self.size - 1):
                output += '\n' + ('---+' * (self.size - 1)) + '---' + '\n'  # line separator

        return output

    def check_coordinates(self, row, col):
        if not self.board[row][col]:
            return True

    def place_mark(self, coord, player):
        self.board[coord[0]][coord[1]] = player
        self.free_spaces -= 1

    def check_win(self, history):
        """ Method used:
        - Verticals & horizontals: counting the marks placed in each row/column, if it's equal to the winning condition,
        winning condition satisfied.
        - Diagonals: same indexes or symmetric indexes.
        Method may seem complex and long for 3x3, but works for any nxn board. """

        if len(history) >= self.size:  # to avoid unnecessary memory usage

            # checking diagonals
            right_to_left = 0  # / symmetric indexes
            left_to_right = 0  # \ same indexes
            for iter_ in range(self.size):
                if (iter_, self.size - 1 - iter_) in history:
                    right_to_left += 1
                if (iter_, iter_) in history:
                    left_to_right += 1

            if right_to_left == self.size or left_to_right == self.size:
                self.winning_combination = True
                return True

            # checking verticals and horizontals
            rows_used = []
            cols_used = []
            for coord in history:
                rows_used.append(coord[0])
                cols_used.append(coord[1])

            for ref in range(self.size):
                if rows_used.count(ref) == self.size or cols_used.count(ref) == self.size:
                    self.winning_combination = True
                    return True

    def blit(self):
        os.system("clear")  # clearing terminal
        print("- TIC TAC TOE by BLDR -\n")
        print(self.gen_display_str())


def get_integer(prompt, max_, min_=0):
    while True:
        n = input(prompt)
        if n.isdigit():
            n = int(n)
            if min_ <= n <= max_:
                return n


def get_human_coordinates(board):
    while True:
        row = get_integer("Row: ", board.size - 1)      # asking for row
        col = get_integer("Column: ", board.size - 1)   # asking for column

        if board.check_coordinates(row, col):
            return row, col
        else:
            print("({}, {}) is already taken.".format(row, col))


def get_ai_coordinates(board):
    return False


def turn(game):

    game.board.blit()  # displaying the board

    if game.AI and game.current_player == 2:    # AI turn
        print("\nAI is thinking . . .")
        time.sleep(2)
        coordinates = get_ai_coordinates(game.board)

    else:                                       # human turn
        print("\n- Player {} -".format(game.current_player))
        coordinates = get_human_coordinates(game.board)         # getting place

    game.board.place_mark(coordinates, game.current_player)     # marking place on the board
    game.update_player_history(coordinates)                     # saving place to history


if __name__ == '__main__':
    os.system("clear")

    print("- TIC TAC TOE by BLDR -\n")

    # getting number of players and creating game object
    main_game = Game(get_integer("Number of Players (only 2 for now): ", 2, min_=2), 3)

    while main_game.board.free_spaces:
        turn(main_game)                                         # processes the turn

        if main_game.board.check_win(main_game.get_history()):  # checks if someone has won
            main_game.board.blit()
            print("\nPlayer {} wins!".format(main_game.current_player))
            break

        main_game.next_player()                                 # moves to the next player (or AI)

    else:
        main_game.board.blit()
        print("\nNo more free spaces - draw!")

    print("\n<return> to exit")
    input()
