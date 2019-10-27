import random
import time
import os

INIT_LIVES = 2
STARTING_ITEMS = 3
SECONDS_PER_ITEM = 2
PASS = 'pass'
FAIL = 'fail'
VALID_INPUTS = [PASS, FAIL]

PRODUCTS = [
    'eggs', 'rice', 'bread', 'apple', 'toilet paper',
    'bananas', 'yogurt', 'chocolate', 'cookies', 'lentils'
]

PLAYER_NAMES = ['player_1', 'player_2']


class Player:
    def __init__(self, name):
        self.name = name
        self.lives = INIT_LIVES
        self.in_game = True
        self.points = 0

    def lose_live(self):
        self.lives -= 1

        if not self.lives:
            self.in_game = False
            input('{} is out of the game...\n'.format(self.name))

    def display_stats(self):
        print('Player: {}\nLives: {}\nPoints: {}'.format(
            self.name, self.lives, self.points
        ))


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
            if player.in_game:
                self.init_grocery_list(player.points)

                clear_screen()
                print('ROUND {}!\nTurn for...\n'.format(self.round))
                player.display_stats()
                input('\n<Enter> when ready!\n')
                self.display_grocery_list()

                result = self.input_result(player.name)

                if result:
                    player.points += 1
                else:
                    player.lose_live()

    def check_any_alive(self):
        return any([player.in_game for player in self.players])

    def init_grocery_list(self, player_points):
        self.grocery_list = []
        number_of_products = STARTING_ITEMS + player_points

        for i in range(number_of_products):
            self.grocery_list.append(
                self.get_item()
            )

    def get_item(self):
        while True:
            product = random.choice(PRODUCTS)
            if product not in self.grocery_list:
                return product

    def display_grocery_list(self):
        print('\nGrocery List\n' + '= ' * 10)
        for product in self.grocery_list:
            print(product)

        time.sleep(SECONDS_PER_ITEM * len(self.grocery_list))
        clear_screen()

    def display_final_results(self):
        clear_screen()
        print('Final Results\n' + '= ' * 10)

        for player in self.players:
            print('{}: {} points'.format(player.name, player.points))

    @staticmethod
    def input_result(player_name):
        while True:
            result = input('Did {} [pass] of [fail]?\n'.format(
                player_name
            )).lower()
            if result in VALID_INPUTS:
                return result == PASS


def clear_screen():
    os.system('clear')


if __name__ == '__main__':
    PLAYERS = [Player(name) for name in PLAYER_NAMES]
    random.shuffle(PLAYERS)
    game = Game(PLAYERS)
    game.run()
