import string
from os import system
from random import choice
from time import sleep


class Game:
    def __init__(self, ):
        self.level = None
        self.possible_levels = ['easy', 'hard']
        self.show_seconds = 2
        self.score = 0
        self.char_set = None
        self.sequence = ''
        self.username = ''
    
    def set_username(self):
        while not self.username:
            username = input('Username: ')
            if username:
                self.username = username
    
    def set_level(self):
        while not self.level:
            level = input('Set level {}: '.format(self.possible_levels)).lower()
            if level in self.possible_levels:
                self.level = level
    
    def set_char_set(self):
        self.char_set = string.ascii_uppercase if self.level == 'hard' else string.digits
    
    def add_char_to_seq(self):
        self.sequence += choice(self.char_set)
    
    def display_seq(self):
        system('clear')
        for char in self.sequence:
            print(char, end=' ')
        print()
        sleep(self.show_seconds)
        system('clear')
    
    @staticmethod
    def get_user_response():
        res = input('Sequence:\n').upper()
        return res.replace(' ', '')
    
    def init_params(self):
        self.set_username()
        self.set_level()
        self.set_char_set()
    
    def run(self):
        system('clear')
        print('- MEMORY GAME -\n')
        self.init_params()
        print('\n{}, game will start in\n'.format(self.username))
        for i in range(3, 0, -1):
            print('{}...'.format(i))
            sleep(1)
        
        while True:
            self.add_char_to_seq()
            self.display_seq()
            res = self.get_user_response()
            if res == self.sequence:
                self.score += 1
            else:
                break
        
        print('\nSequence was: {}\nGame ended, final score -> {}'.format(self.sequence, self.score))


if __name__ == '__main__':
    game = Game()
    game.run()
