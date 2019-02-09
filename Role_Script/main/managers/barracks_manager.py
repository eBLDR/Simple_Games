class Barracks:
    def __init__(self, player):
        self.player = player

    def run(self):
        # TODO: for testing
        if self.player.skill_points_to_use:
            self.player.upgrade_stat()
        else:
            input('NO POINTS')
