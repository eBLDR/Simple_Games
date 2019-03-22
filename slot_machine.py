import os
import random
import sys
import time


class Slot:
    def __init__(self):
        self.options = ['$',
                        '7', '7',
                        'A', 'A', 'A',
                        'B', 'B', 'B',
                        'C', 'C', 'C',
                        'X', 'X', 'X', 'X', 'X', 'X']

    def spin(self):
        return random.choice(self.options)


class SlotMachine:
    def __init__(self):
        self.number_of_slots = 3
        self.slots = [Slot() for _ in range(self.number_of_slots)]

        self.delay_time = 0.5

        self.bet = 5

        self.rewards = {
            '$': 1500,
            '7': 500,
            'A': 50,
            'B': 50,
            'C': 50,
            'X': 10
        }

    def spin_all(self):
        return [slot.spin() for slot in self.slots]

    @staticmethod
    def is_winning_combination(combination):
        for n in combination:
            if combination[0] != n:
                return False

        return True

    def calculate_reward(self, combination):
        if self.is_winning_combination(combination):
            return self.rewards.get(combination[0])

        return 0

    def play(self, player):
        player.money -= self.bet
        print('Spinning...!\n')
        time.sleep(self.delay_time)
        combination = self.spin_all()
        print(combination)
        reward = self.calculate_reward(combination)
        input('You win: {}\n'.format(reward))
        player.money += reward
        os.system('clear')


class Player:
    def __init__(self):
        self.money = 50


if __name__ == '__main__':
    john = Player()
    slot_machine = SlotMachine()

    print('==== SLOT MACHINE ====\n')

    while True:
        while True:
            print('Money: {}\n\n<P> to Play\n<E> to Exit'.format(john.money))
            action = input('>>> ').lower()
            if action in ['p', 'e']:
                break

        if action == 'e':
            print('\nEnjoy your reward.')
            sys.exit()

        if john.money < slot_machine.bet:
            input('Not enough money to play!')
            continue

        slot_machine.play(john)
