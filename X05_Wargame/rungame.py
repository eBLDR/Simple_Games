"""
ALERT: Old code, this game was made as a learning project.
TODO: Main refactor pending

X-05 WARGAME
"""
import pygame

from data import commons

MOUSE_LEFT = 1  # by default
MOUSE_RIGHT = 3  # by default


def main():
    commons.init_game()

    while True:
        mouse_x, mouse_y = 0, 0
        mouse_clicked = False
        arrow_pressed = None  # D, W, A, S

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                commons.exit_game()

            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos

                if event.button == MOUSE_LEFT:
                    mouse_clicked = 'LEFT'

                elif event.button == MOUSE_RIGHT:
                    mouse_clicked = 'RIGHT'

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    arrow_pressed = 'D'
                elif event.key == pygame.K_w:
                    arrow_pressed = 'W'
                elif event.key == pygame.K_a:
                    arrow_pressed = 'A'
                elif event.key == pygame.K_s:
                    arrow_pressed = 'S'

                elif event.key == pygame.K_SPACE:
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

        commons.run_game(mouse_x, mouse_y, mouse_clicked, arrow_pressed)


# ------------------------------ EXECUTE
if __name__ == '__main__':
    pygame.init()
    main()
