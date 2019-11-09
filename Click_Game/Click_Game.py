# Created and developed by
# BLDR, 2014
import random
import sys

import pygame
from pygame.locals import *

pygame.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Game:
    def __init__(self):
        self.clicks = 0
        self.corpses = 0
        self.multiplier = 1
        self.tip = ''
        self.tip_tl = (0, 0)


class WeirdGuy:
    def __init__(self):
        random_x = random.randint(40, 1000)
        random_y = random.randint(40, 500)
        self.img = pygame.image.load('img/001_64.png')
        self.surf = self.img.get_rect(center=(random_x, random_y))
        self.exists = True


def blit(size):
    click_counter_surf = click_counter.render('Clicks  %i' % game.clicks, True, WHITE)
    corpses_counter_surf = corpses_counter.render('Corpses  %i' % game.corpses, True, WHITE)
    multiplier_text_surf = multiplier_text.render('x %i' % game.multiplier, True, WHITE)
    multiplier_text_rect = multiplier_text_surf.get_rect(topleft=(10, size[1] - 60))
    screen.blit(background, background_rect)
    screen.blit(my_friend, my_friend_surf)
    screen.blit(click_counter_surf, click_counter_rect)
    screen.blit(corpses_counter_surf, corpses_counter_rect)
    screen.blit(multiplier_text_surf, multiplier_text_rect)


def tips(number_corpses):
    game.tip = ''
    game.tip_tl = (0, 0)
    if number_corpses < 10:
        game.tip = 'Click this guy'
        game.tip_tl = (size[0] / 2 + 100, size[1] / 2 - 100)

    elif number_corpses < 30:
        game.tip = 'Keep clicking'
        game.tip_tl = (size[0] / 2 + 100, size[1] / 2 + 100)

    elif number_corpses < 60:
        game.tip = 'More'
        game.tip_tl = (size[0] / 2 - 150, size[1] / 2 + 100)

    elif number_corpses < 96:
        game.tip = 'MORE'
        game.tip_tl = (size[0] / 2 - 150, size[1] / 2 - 100)

    tip_text_surf = tip_text.render(game.tip, True, RED)
    tip_text_rect = tip_text_surf.get_rect(topleft=game.tip_tl)
    screen.blit(tip_text_surf, tip_text_rect)


def blit_weird_guys():
    for j in WEIRD_GUYS:
        if j.exists is True:
            screen.blit(j.img, j.surf)


def check_main_collision(x, y):
    if my_friend_surf.collidepoint(x, y):
        if my_friend_mask.get_at((x - my_friend_top_left[0], y - my_friend_top_left[1])):
            game.clicks += 1
            game.corpses += (1 * game.multiplier)

            if game.corpses > 95 and game.clicks % 12 == 0:
                wg = WeirdGuy()
                WEIRD_GUYS.append(wg)


def check_weird_guy_collision(x, y):
    for i in WEIRD_GUYS:
        if i.exists is True:
            if i.surf.collidepoint(x, y):
                i.exists = False
                game.multiplier += 1


def clean_weird_guy_list():
    for i in range(len(WEIRD_GUYS) - 1, -1, -1):
        if WEIRD_GUYS[i].exists is False:
            del WEIRD_GUYS[i]


def main():
    while True:
        mouse_x = 0
        mouse_y = 0

        blit(size)
        tips(game.corpses)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos

        check_main_collision(mouse_x, mouse_y)
        check_weird_guy_collision(mouse_x, mouse_y)
        clean_weird_guy_list()
        blit_weird_guys()

        pygame.display.update()


if __name__ == '__main__':
    game = Game()

    WEIRD_GUYS = []

    background = pygame.image.load('bg/bg_1024x576.jpg')
    background_rect = background.get_rect()
    size = (W, H) = background.get_size()

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Click Game")

    my_friend = pygame.image.load('img/008_256.png')  # .convert_alpha()
    my_friend_surf = my_friend.get_rect(center=(W / 2, H / 2))
    my_friend_mask = pygame.mask.from_surface(my_friend)
    my_friend_top_left = my_friend_surf.topleft

    click_counter = pygame.font.Font('font/28_Days_Later.ttf', 16)
    click_counter_surf = click_counter.render('Clicks  %i' % game.clicks, True, WHITE)
    click_counter_rect = click_counter_surf.get_rect(topleft=(10, 45))

    corpses_counter = pygame.font.Font('font/28_Days_Later.ttf', 32)
    corpses_counter_surf = corpses_counter.render('Corpses  %i' % game.corpses, True, WHITE)
    corpses_counter_rect = corpses_counter_surf.get_rect(topleft=(10, 10))

    multiplier_text = pygame.font.Font('font/28_Days_Later.ttf', 52)
    multiplier_text_surf = multiplier_text.render('x %i' % game.multiplier, True, WHITE)
    multiplier_text_rect = multiplier_text_surf.get_rect(topleft=(10, size[1] - 60))

    tip_text = pygame.font.Font('font/28_Days_Later.ttf', 24)
    tip_text_surf = tip_text.render(game.tip, True, RED)
    tip_text_rect = tip_text_surf.get_rect(topleft=game.tip_tl)

    # pygame.mixer.music.load('sound/chopin_p2.mid')
    # pygame.mixer.music.play(-1,0.0)

    # bomb_sound = pygame.mixer.Sound('sound\\Atomic_Bomb.wav')

    main()
