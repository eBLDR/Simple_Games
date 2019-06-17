"""
X-05 WARGAME

MAIN FILE
"""

# ------------------------------ IMPORTS

import pygame
from pygame.locals import *

pygame.init()

from data import commons

# ------------------------------ CONTROL CONSTANTS
MOUSE_LEFT = 1  # by default
MOUSE_RIGHT = 3  # by default


# ------------------------------ MAIN LOOP
def main():
    commons.init_game()

    while True:
        mouse_x, mouse_y = 0, 0
        mouse_clicked = arrows_pressed = False
        arrows = [False, False, False, False]  # D, W, A, S

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                commons.exit_game()

            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos

            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos

                if event.button == MOUSE_LEFT:
                    mouse_clicked = 'LEFT'

                elif event.button == MOUSE_RIGHT:
                    mouse_clicked = 'RIGHT'

            elif event.type == KEYUP:
                if event.key == K_d:
                    arrows_pressed, arrows[0] = True, True
                elif event.key == K_w:
                    arrows_pressed, arrows[1] = True, True
                elif event.key == K_a:
                    arrows_pressed, arrows[2] = True, True
                elif event.key == K_s:
                    arrows_pressed, arrows[3] = True, True

                elif event.key == K_SPACE:
                    commons.next_phase()

        keys = pygame.key.get_pressed()

        direction = None

        if keys[pygame.K_RIGHT]:
            direction = 'right'
        if keys[pygame.K_UP]:
            direction = 'up'
        if keys[pygame.K_LEFT]:
            direction = 'left'
        if keys[pygame.K_DOWN]:
            direction = 'down'

        if direction:
            commons.move_camera(direction)

        commons.go(mouse_x, mouse_y, mouse_clicked, arrows_pressed, arrows)


# ------------------------------ EXECUTE
if __name__ == '__main__':
    main()
