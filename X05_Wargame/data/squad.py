import pygame

from data import codex


class Squad:
    def __init__(self, player, name, units, init_x, init_y, init_direction):
        self.player = int(player)
        self.name = name.lower()
        self.units = int(units)
        self.direction = init_direction

        self.img = None
        self.update_img(update=False)

        self.pos = self.deploy_squad(init_x, init_y)  # center

        self.stats = codex.get_stats(name)
        self.category = codex.get_category(name)

        self.mouse_over = False
        self.is_selected = False
        self.engaged = False
        self.can_move = True
        self.can_rotate = True
        self.can_range_attack = True
        self.can_melee_attack = True

        # self.front = -
        # self.engage = {'front':False,'back':False,'left':False,'right':False}
        # self.get_away = False

    def __str__(self):
        return 'Player %i / %s / %i units' % (self.player, self.name, self.units)

    def update_img(self, update=True):
        if self.units == 1:
            try:
                img = pygame.image.load('data/src/img/%s_individual.png' % self.name).convert_alpha()
            except:
                try:
                    img = pygame.image.load('data/src/img/%s_tiny.png' % self.name).convert_alpha()
                except:
                    img = pygame.image.load('data/src/img/%s_small.png' % self.name).convert_alpha()
        elif 1 < self.units <= 8:
            try:
                img = pygame.image.load('data/src/img/%s_tiny.png' % self.name).convert_alpha()
            except:
                img = pygame.image.load('data/src/img/%s_small.png' % self.name).convert_alpha()
        elif 8 < self.units <= 16:
            img = pygame.image.load('data/src/img/%s_small.png' % self.name).convert_alpha()
        elif 16 < self.units <= 24:
            img = pygame.image.load('data/src/img/%s_medium.png' % self.name).convert_alpha()
        elif 24 < self.units <= 36:
            img = pygame.image.load('data/src/img/%s_big.png' % self.name).convert_alpha()
        elif self.units > 36:
            try:
                img = pygame.image.load('data/src/img/%s_huge.png' % self.name).convert_alpha()
            except:
                img = pygame.image.load('data/src/img/%s_big.png' % self.name).convert_alpha()

        self.img = pygame.transform.rotate(img, self.direction - 90)

        if update:
            self.generate_rect()

    def deploy_squad(self, init_x, init_y):
        squad_rect = self.img.get_rect(center=(init_x, init_y))
        return [[init_x, init_y], squad_rect]

    def move_squad(self, x, y):
        self.pos[0] = [x, y]
        self.generate_rect()

    def change_direction(self, new_dir):
        rotate_angle = new_dir - self.direction
        self.img = pygame.transform.rotate(self.img, rotate_angle)
        self.generate_rect()
        self.direction = new_dir

    def generate_rect(self):
        self.pos[1] = self.img.get_rect(center=(self.pos[0][0], self.pos[0][1]))

    def get_mov(self):
        return self.stats[0]  # max movement (pix)

    def get_mA(self):
        return self.stats[1]  # melee ability, prob of impacts/max=10

    def get_dA(self):
        return self.stats[2]  # distance ability, prob of impacts/max=10

    def get_dR(self):
        return self.stats[3]  # max distance range atk (pix)

    def get_S(self):
        return self.stats[4]  # strength

    def get_R(self):
        return self.stats[5]  # resistance

    def get_front(self):
        if self.units <= 6:
            return self.units
        elif self.units >= 54:
            return 30
        else:
            return 6 + int((self.units - 6) / 2)

    """
    def set_front(self):
        front = 5
        if front > self.units:
            front = self.units
        return front
    
    # def show_move_range(self): ?

    # def show_attack_range(self): ?

    # def change_front(self):

    # def getting_away():
    """
