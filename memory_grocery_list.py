import os
import random
import time

# TODO: finish flash feature
# TODO: feature distractions
# TODO: improve exit() when level higher than len(ITEMS)

# Init set up
INIT_LIVES = 2
INIT_FLASHES = 2
STARTING_ITEMS = 12
SECONDS_PER_ITEM = 2

PASS = 'pass'
FAIL = 'fail'
VALID_INPUTS = {
    'p': PASS,
    'f': FAIL,
}

# ITEMS = [
#     'mobile', 'almond', 'oats', 'skipping rope', 'yoga block',
#     'shoe spray', 'lemon', 'battery', 'candle', 'cup', 'frisbee',
#     'tupperware', 'book', 'bandage', 'pen', 'pencil', 'cookies',
#     'paper roll', 'watch', 'umbrella', 'cutlery'
# ]


ITEMS = [
    'mobil', 'ametlla', 'avena', 'corda', 'ioga bloc',
    'spray', 'llimona', 'piles', 'espelma', 'tassa', 'frisbee',
    'tupperware', 'llibre', 'vena', 'boli', 'llapis', 'galetes',
    'rotllo paper', 'rellotge', 'paraigues', 'coberts'
]

PLAYER_NAMES = ['Sarahhh', 'Princess Go (AKA DP)', 'PRO/BRO Joan', 'BLDR']


class Player:
    def __init__(self, name):
        self.name = name
        self.lives = INIT_LIVES
        self.flashes = INIT_FLASHES
        self.in_game = True
        self.points = 0

    def lose_live(self):
        self.lives -= 1

        if not self.lives:
            self.in_game = False
            input(f'{self.name} is out of the game...\n')

    def display_stats(self):
        print(f'Player: {self.name}\nLives: {self.lives}\nPoints: {self.points}')


class Game:
    def __init__(self, players):
        self.playing = True
        self.players = players
        self.round = 1
        self.grocery_list = None

    def run(self):
        while self.playing:
            self.play_round()

            if not self.check_any_alive():
                self.playing = False
                break
                # continue

            self.round += 1

        self.display_final_results()

    def play_round(self):
        for player in self.players:
            if not player.in_game:
                continue

            number_of_items = STARTING_ITEMS + player.points

            clear_screen()
            print(f'ROUND {self.round}!\nTurn for...\n')

            # Player has reached a level where according number of items cannot be handled
            if number_of_items > len(ITEMS):
                print(f'{player.name}, you are too smart!\nAdd more items to the list next time!\n'
                      'You are out of this game.')

                enter_to_continue()

                player.in_game = False
                continue

            player.display_stats()
            enter_to_continue()

            self.init_grocery_list(number_of_items)
            self.display_grocery_list(number_of_items)

            print('Go and pick the items!')
            enter_to_continue()

            self.display_grocery_list(number_of_items, sleep_=False)

            result = self.input_result(player.name)

            if result:
                player.points += 1
            else:
                player.lose_live()

    def check_any_alive(self):
        return any([player.in_game for player in self.players])

    def init_grocery_list(self, number_of_items):
        self.grocery_list = []

        for i in range(number_of_items):
            self.grocery_list.append(
                self.get_item()
            )

    def get_item(self):
        while True:
            item = random.choice(ITEMS)
            if item not in self.grocery_list:
                return item

    def display_grocery_list(self, number_of_items, sleep_=True):
        print(f'\nGrocery List - ({number_of_items})\n' + '= ' * 10)
        for item in self.grocery_list:
            print(item)

        if sleep_:
            time.sleep(SECONDS_PER_ITEM * len(self.grocery_list))
            clear_screen()

    def display_final_results(self):
        clear_screen()
        print('Final Results\n' + '= ' * 10 + f'\nTotal Rounds: {self.round}')

        for player in self.players:
            print(f'{player.name}: {player.points} points.')

        print()
        enter_to_continue()

    @staticmethod
    def input_result(player_name):
        print()

        while True:
            result = input(f'Did {player_name} [p]ass or [f]ail?\n').lower()

            if result in VALID_INPUTS.keys():
                return VALID_INPUTS[result] == PASS


def clear_screen():
    os.system('clear')


def enter_to_continue():
    input('\n<Enter> to continue...\n')


if __name__ == '__main__':
    print(f'\n--- MEMORY GROCERY LIST ---\n\nThere are {len(ITEMS)} items.')
    enter_to_continue()

    PLAYERS = [Player(name) for name in PLAYER_NAMES]
    random.shuffle(PLAYERS)
    game = Game(PLAYERS)
    game.run()
