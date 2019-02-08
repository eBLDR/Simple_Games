import os

from main.ui import graphics_maps


def display_world_map():
    os.system('clear')
    print(graphics_maps.displays_places.get('world_map'))
