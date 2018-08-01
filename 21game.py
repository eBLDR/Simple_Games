# By turns (AI, user) withdraw 1 or 2 units from the total of 21,
# taking the last unit (zero left), is a win.

import random


def IA_turn(total):
    if (total-1) % 3 == 0:
        r = 1
        
    elif (total-2) % 3 == 0:
        r = 2
                
    else:
        r = random.randint(1, 2)

    print('\nIA takes:', r)

    return r


def user_turn():
    while True:
        n = input('\nUser takes (1 or 2): ')
        if n.isdigit():
            n = int(n)
            if n == 1 or n == 2:
                return n


def check_win(total):
    return True if total <= 0 else False


def print_remainding(total):
    print("{} remainding.".format(total))


def game():
    total = 21
    
    print ('21 GAME\n\nPress <enter> to START')
    input()

    print_remainding(total)

    print ("\nIA Starts...")

    while True:
        total -= IA_turn(total)
        print_remainding(total)
        if check_win(total):
            print('\n- DEFEAT, IA WIN -')
            break

        total -= user_turn()
        print_remainding(total)
        if check_win(total):
            print ('\n- VICTORY, USER WIN -')
            break


game()
