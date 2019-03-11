import random
import curses


def main(stdscr_):
    std_scr = curses.initscr()
    curses.curs_set(0)
    console_height, console_width = std_scr.getmaxyx()
    screen = curses.newwin(console_height, console_width, 0, 0)
    screen.keypad(1)
    screen.timeout(100)

    # Snake
    snk_x = console_width // 4
    snk_y = console_height // 2
    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2]
    ]

    # Display first food in the center
    food = [console_height // 2, console_width // 2]
    screen.addch(food[0], food[1], curses.ACS_PI)

    # Start by going right
    key = curses.KEY_RIGHT

    while True:
        next_key = screen.getch()
        key = key if next_key == -1 else next_key

        # Collision
        if snake[0][0] in [0, console_height] or snake[0][1] in [0, console_width] or snake[0] in snake[1:]:
            curses.endwin()
            quit()

        new_head = [snake[0][0], snake[0][1]]

        # Event listening
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        if key == curses.KEY_UP:
            new_head[0] -= 1
        if key == curses.KEY_LEFT:
            new_head[1] -= 1
        if key == curses.KEY_RIGHT:
            new_head[1] += 1

        snake.insert(0, new_head)

        # Eating food
        if snake[0] == food:
            food = None
            while food is None:
                new_food = [
                    random.randint(1, console_height - 1),
                    random.randint(1, console_width - 1)
                ]
                food = new_food if new_food not in snake else None

            screen.addch(food[0], food[1], curses.ACS_PI)

        else:
            tail = snake.pop()
            screen.addch(tail[0], tail[1], ' ')

        screen.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)


curses.wrapper(main)
