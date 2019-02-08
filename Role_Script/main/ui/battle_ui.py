import math
import os


def separation_bar():
    return '\n' + '#' * 40 + '\n\n'


def generate_progress_bar(current: int, maximum: int):
    max_spaces = 20
    fill = math.ceil(current * max_spaces / maximum)
    empty = max_spaces - fill
    return '[' + ('=' * fill) + ' ' * empty + ']' + ' ({}/{})'.format(current, maximum)


def health_bar(being):
    return '\033[92mHealth ' + generate_progress_bar(being.health, being.max_health) + '\033[0m'


def energy_bar(being):
    return '\033[94mEnergy ' + generate_progress_bar(being.energy, being.max_energy) + '\033[0m'


def display_enemy(enemy):
    return '\n' + health_bar(enemy) + '\n' + energy_bar(enemy) + '\nName: {} | Level: {}'.format(enemy.name, enemy.level) + '\n\n' + enemy.display


def display_player_stats(player):
    return health_bar(player) + '\n' + energy_bar(player)


def display_user_options(user_options: list):
    return '\n' + ' | '.join(['{}'.format(option.title()) for option in user_options])


def display_battle_ui(player, enemy, user_options: list = None, info: str = None):
    os.system('clear')
    str_ = display_enemy(enemy) + separation_bar() + display_player_stats(player) + '\n'
    if user_options:
        str_ += display_user_options(user_options) + '\n'
    print(str_)
    if info:
        input('\033[93m{}\033[0m\n\n> '.format(info))
