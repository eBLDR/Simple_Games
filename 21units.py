# '21 units' game, by BLDR
# By turns (AI, user) withdraw 1 or 2 units from the total of 21,
# taking the last unit (zero left), is a win.

import random


class Game:
    def __init__(self):
        self.units = 21
        self.playing = True

    def display_ui(self, msg=''):
        prompt = '{}\n{} units remaining.'.format(msg, self.units) if msg else '{} units remaining.'.format(self.units)
        print(prompt + '\n' + '=' * 20)

    def check_win(self):
        check = True if self.units <= 0 else False
        if check:
            self.playing = False
        return check

    def ai_turn(self):
        if (self.units - 1) % 3 == 0:
            n = 1
        elif (self.units - 2) % 3 == 0:
            n = 2
        else:
            n = random.randint(1, 2)
        self.units -= n
        msg = '\nAI takes: ' + str(n)
        self.display_ui(msg)

    def user_turn(self):
        while True:
            n = input('\nUser takes (1 or 2): ')
            if n.isdigit():
                n = int(n)
                if n == 1 or (n == 2 and self.units > 1):
                    break
        self.units -= n
        self.display_ui()

    def play(self):
        input('21 GAME by BLDR\n\nPress <enter> to START\n')
        self.display_ui()
        print ('IA Starts...')
        while self.playing:
            self.ai_turn()
            if self.check_win():
                input('\n- DEFEAT, AI WIN -\n\n<enter>')
                break
            self.user_turn()
            if self.check_win():
                input('\n- VICTORY, USER WIN -\n\n<enter>')


if __name__ == '__main__':
    game = Game()
    game.play()
