class Player:
    def __init__(self, number, name):
        self.number = number
        self.name = name
        # self.icon = self.set_icon()
        self.is_death = False
        self.army = []

    def __str__(self):
        return 'Player %i / %s' % (self.number, self.name)

    def set_number(self, num):
        self.number = num

    # def set_icon(self):

    def add_squad(self, squad):
        self.army.append(squad)

    def lose_squad(self, squad):
        index = self.army.index(squad)
        del self.army[index]
