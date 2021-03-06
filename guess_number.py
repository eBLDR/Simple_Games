# Guessing number, by BLDR
# User has to guess a random number from 1 to 100 generated by AI, using a maximum of 7 guesses
import random


class Game:
    def __init__(self):
        self.remaining_guesses = 7
        self.random_number = self.set_random_number()

    @staticmethod
    def set_random_number():
        # Returns a random number in range [1, 100]
        return random.randint(1, 100)

    def get_user_guess(self):
        # Returns user's valid integer input
        while True:
            n = input('{} guesses left. Number: '.format(self.remaining_guesses))
            if n.isdigit():
                n = int(n)
                if 0 < n <= 100:
                    return n

    def play(self):
        # Main loop
        print('Guessing Game, by BLDR\n\nGuess a random number from 1 to 100 in maximum 7 guesses!\n')
        while self.remaining_guesses > 0:
            guess = self.get_user_guess()
            if guess == self.random_number:
                input('\n- Correct guess! -\n\n<enter>')
                break
            elif guess > self.random_number:
                print('Guess lower!\n')
            else:
                print('Guess higher!\n')

            self.remaining_guesses -= 1
        else:
            input('\n- No more guesses... -\n\n<enter>')


if __name__ == '__main__':
    game = Game()
    game.play()
