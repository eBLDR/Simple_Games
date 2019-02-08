from main.ui import map_ui


class WorldMap:
    def __init__(self, options):
        self.options = options

    def run(self):
        map_ui.display_world_map()
        return self.get_option()

    def get_option(self):
        while True:
            option = input('> ').lower()
            if option in self.options:
                return option
