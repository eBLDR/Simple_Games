import copy
import random

from main.species.base_being import Being
from main.ui import battle_ui
from main.ui.graphics_beings import displays_beings


class Battle:
    def __init__(self, player):

        self.player = player
        self.enemy = None

        self.options = ['attack', 'escape']

    def fight(self):
        self.generate_enemy()

        in_battle = True

        while in_battle:
            self.display_ui(user_options=self.options)
            player_action = self.get_player_action()

            if player_action == 'attack':
                damage = self.player.attack(self.enemy)
                prompt = '{} has dealt {} damage.'.format(self.player.name, damage)
                self.display_ui(info=prompt)

                if not self.enemy.is_alive():
                    exp = self.player.has_killed(self.enemy)
                    prompt = '{} is dead! You have gained {}xp.'.format(self.enemy.name, exp)
                    in_battle = False
                else:
                    damage = self.enemy.attack(self.player)
                    prompt = '{} has dealt {} damage.'.format(self.enemy.name, damage)
                self.display_ui(info=prompt)

                if not self.player.is_alive():
                    prompt = 'You died!!!'
                    in_battle = False
                    self.display_ui(info=prompt)

            elif player_action == 'escape':
                success = self.player.escape(self.enemy)
                if success:
                    in_battle = False
                    prompt = 'You have escaped!'
                else:
                    prompt = '{} is too fast, cannot escape!'.format(self.enemy.name)
                self.display_ui(info=prompt)

    def generate_enemy(self):
        self.enemy = copy.deepcopy(Being(name=random.choice(list(displays_beings.keys())), experience=self.player.experience // 4))

    def display_ui(self, user_options=None, info=None):
        battle_ui.display_battle_ui(self.player, self.enemy, user_options=user_options, info=info)

    def get_player_action(self):
        while True:
            action = input('> ').lower()
            if action in self.options:
                return action
