# Simple Battleship version, by BLDR.

import random


def generate_board(size):
    """
    Generates board with a given size*size
    """
    matrix = []
    for i in range(size):
        matrix.append([])
        for j in range(size):
            matrix[i].append("O")
    return matrix


def show_board(board):
    """
    Displays board.
    """
    print('   ', end='')
    for i in range(len(board)):
        print(i + 1, end=' ')
    print('\n')
    for j, row in enumerate(board):
        print(j + 1, end='  ')
        for value in row:
            print(value, end=' ')
        print()

            
def ship_position(board):
    """
    Returns a random position (x, y).
    """
    row = random.randint(0, len(board) - 1)
    column = random.randint(0, len(board) - 1)
    return row, column


def user_coordinates(board):
    """
    Return a valid position (x, y) given by the user.
    """
    print()
    coord = []
    while len(coord) < 2:
        if len(coord) == 0:
            prompt = "Row? "
        else:
            prompt = "Column? "
        f = input(prompt)
        if f.isdigit():
            f = int(f) - 1
            if 0 <= f < len(board):
                coord.append(f)
            else:
                print("Out of range.")
        else:
            print("Must be integer.")

    print()
    return tuple(coord)


def game(board):
    """
    Main loop.
    """
    print("- BATTLESHIP -\n")
    missile = len(board) + 2
    enemy_ship = ship_position(board)
    show_board(board)
    while missile > 0:
        target = user_coordinates(board)
        if target == enemy_ship:
            board[enemy_ship[0]][enemy_ship[1]] = "#"
            show_board(board)
            print("\nEnemy ship destroyed!\n\n- VICTORY! -")
            break

        elif target != enemy_ship:
            if board[target[0]][target[1]] == "O":
                board[target[0]][target[1]] = "X"
                show_board(board)
                missile -= 1
                print('\nWater! Remaining missile/s {}'.format(missile))
            else:
                print("Coordinates already attacked...")

    else:
        print("\nNo missiles left, enemy ship still sailing...\n\n- DEFEAT! -")

    
M = 4  # size of the board

BOARD = generate_board(M)

game(BOARD)
