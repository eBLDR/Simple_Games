#! /usr/bin/python

import os
import sys
import random
import string

from graphics import HANGMANPICS
from wordset import WORDSET


class Hangman:

    def __init__(self):
        self.secret_word = ''
        self.guessing_word = ''
        
        self.hangman_pics = HANGMANPICS
        
        self.fails = 0
        self.max_fails = len(self.hangman_pics) - 1
        
        self.valid_letters = set(string.ascii_lowercase)
        self.used_letters = set()
    
    def display_ui(self):
        os.system('clear')
        print('--- Hangman by BLDR ---')
        print("=" * 24)
        print(self.hangman_pics[self.fails])
        print()
        print(self.guessing_word)
        print("=" * 24)
        
    def set_secret_word(self):
        self.secret_word = random.choice(WORDSET).lower()
    
    def generate_empty_guessing_word(self):
        for i in range(len(self.secret_word)):
            if self.secret_word[i] == ' ':
                self.guessing_word += ' '
            else:
                self.guessing_word += '-'
    
    def get_new_letter(self):
        while True:
            prompt = 'Choose a letter: '
            letter = input(prompt).lower()
            if letter == 'quit':
                sys.exit(0)
            if self.verify_input(letter):
                return letter
    
    def verify_input(self, letter):        
        if len(letter) == 1 and letter in self.valid_letters:
            if letter not in self.used_letters:
                return True
            else:
                print('{} was already chosen.'.format(letter))
                return False
        else:
            print('Invalid input.')
            return False

    def process_letter(self, letter):
        tmp = ''
        found = False
        for i in range(len(self.secret_word)):
            if self.secret_word[i] == letter:
                found = True
                tmp += letter
            else:
                tmp += self.guessing_word[i]
        self.used_letters.add(letter)
        self.guessing_word = tmp          
        if not found:
            self.fails += 1
    
    def check_win(self):
        return True if self.guessing_word == self.secret_word else False
    
    def init(self):
        self.set_secret_word()
        self.generate_empty_guessing_word()
    
    def round(self):
        letter = self.get_new_letter()
        self.process_letter(letter)
        
    def run(self):
        self.init()
        self.display_ui()
        while self.fails < self.max_fails:
            self.round()
            self.display_ui()
            if self.check_win():
                print('You win!')
                break
        else:
            print('You lost...')
            print('Secret word: {}'.format(self.secret_word))


if __name__ == '__main__':
    game = Hangman()
    game.run()
