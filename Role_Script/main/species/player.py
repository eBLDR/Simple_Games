import os

from main.species.base_being import Being
from main.ui import player_ui


class Player(Being):

    def __init__(self, name):
        super().__init__(name=name)
        self.enemies_killed = 0
        self.skill_points_to_use = 10

        # Objects
        self.inventory = []

        self.distribute_init_skill_points()

    def distribute_init_skill_points(self):
        while self.skill_points_to_use > 0:
            self.upgrade_stat()
            self.skill_points_to_use -= 1

    def level_up(self):
        self.skill_points_to_use += 1

    def upgrade_stat(self):
        os.system('clear')
        stats_dict = self.stats_to_dict()
        player_ui.display_stats(stats_dict)
        while True:
            stat = input('> ').lower().replace(' ', '_')
            if stat in self.stats_to_upgrade:
                self._upgrade_stat(stat)
                break

    def escape(self, chaser):
        return self.agility >= chaser.agility

    def has_killed(self, enemy):
        exp = enemy.give_experience()
        self.experience += exp
        return exp
