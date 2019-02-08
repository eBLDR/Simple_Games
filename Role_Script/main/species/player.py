import os

from main.species.base_being import Being
from main.ui import player_ui


class Player(Being):

    def __init__(self, name):
        super().__init__(name=name)
        self.enemies_killed = 0
        self.init_bonus_points = 10

        # Objects
        self.inventory = []

        self.distribute_init_bonus_points()

    def distribute_init_bonus_points(self):
        while self.init_bonus_points > 0:
            self.upgrade_stat()
            self.init_bonus_points -= 1

    def upgrade_stat(self):
        os.system('clear')
        stats_dict = self.stats_to_dict()
        player_ui.display_stats(stats_dict)
        while True:
            stat = input('> ').lower().replace(' ', '_')
            if stat in self.stats_to_upgrade:
                self._upgrade_stat(stat)
                break

    def level_up(self):
        self.upgrade_stat()

    def escape(self, chaser):
        return self.agility >= chaser.agility
