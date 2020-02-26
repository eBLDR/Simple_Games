import random

import pygame

# Constants
BLACK = (255, 255, 255)
WHITE = (0, 0, 0)


class Counter:
    def __init__(self):
        self.jump = 10  # Multiplier appears
        self.clicks = 0
        self.multiplier = 1

        self.points = 0


class Multiplier:
    def __init__(self):
        self.show = False
        self.position = None

    def reset_position(self):
        margin = 50

        x = random.randint(margin, screen_size[0] - margin)
        y = random.randint(margin, screen_size[1] - margin)

        self.position = (x, y)

    def appear(self):
        self.show = True
        self.reset_position()

    def disappear(self):
        self.show = False


class HUB:
    x_pos = 20
    y_pos = 20
    line_jump = 20
    font_name = 'Consolas'
    font_size = 24

    def __init__(self, counter):
        self.counter = counter
        self.font = pygame.font.SysFont(self.font_name, self.font_size)

    def render(self):
        text_bulk = [
            f'Clicks: {self.counter.clicks}',
            f'Multiplier: {self.counter.multiplier}',
            f'Points: {self.counter.points}',
        ]

        for index, text_raw in enumerate(text_bulk):
            text = self.font.render(text_raw, True, BLACK)
            screen.blit(text, (self.x_pos, self.y_pos * (index + 1)))


def update_counter(counter):
    counter.clicks += 1
    counter.points += counter.multiplier

    if counter.clicks % counter.jump == 0:
        multiplier.appear()


pygame.init()

screen_size = (500, 500)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Simple Clicker')

# Clicker stuff
clicker_filename = 'src/clicker.png'
clicker_position = (220, 210)
clicker = pygame.image.load(clicker_filename)

# Multiplier stuff
multiplier_filename = 'src/mult.png'
multiplier_image = pygame.image.load(multiplier_filename)

# General variables
run = True
player_counter = Counter()
multiplier = Multiplier()
hub = HUB(player_counter)

# Main loop
while run:
    screen.fill(WHITE)
    screen.blit(clicker, clicker_position)
    hub.render()

    if multiplier.show:
        screen.blit(multiplier_image, multiplier.position)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                if clicker.get_rect(topleft=clicker_position).collidepoint(event.pos):
                    update_counter(player_counter)

                if multiplier.show:
                    if multiplier_image.get_rect(topleft=multiplier.position).collidepoint(event.pos):
                        player_counter.multiplier += 1
                        multiplier.disappear()

    pygame.display.update()

pygame.quit()
