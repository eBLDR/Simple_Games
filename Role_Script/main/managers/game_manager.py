import os
import sys

from main.managers.barracks_manager import Barracks
from main.managers.battle_manager import Battle
from main.managers.world_map_manager import WorldMap
from main.species.player import Player


class Game:
    def __init__(self):
        self.options = ['exit', 'battle', 'barracks']

        self.intro()

        self.player = self.initialise_player()

        # Managers
        self.world_map_manager = WorldMap(self.options)
        self.barracks_manager = Barracks(self.player)
        self.battle_manager = Battle(self.player)

    def run(self):
        while True:
            next_ = self.world_map()
            if next_ == 'exit':
                self._exit()
            elif next_ == 'barracks':
                self.barracks()
            elif next_ == 'battle':
                self.battle()

    @staticmethod
    def _exit():
        sys.exit()

    @staticmethod
    def intro():
        os.system('clear')
        print('- ROLE SCRIPT GAME -\n')

    def initialise_player(self):
        name = self.get_player_name()
        return Player(name=name)

    @staticmethod
    def get_player_name():
        while True:
            name = input('Player name: ')
            if name.replace(' ', ''):
                return name

    def world_map(self):
        return self.world_map_manager.run()

    def barracks(self):
        self.barracks_manager.run()

    def battle(self):
        self.battle_manager.fight()
