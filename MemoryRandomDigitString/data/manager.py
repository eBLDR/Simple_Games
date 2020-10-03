import json
import os
import random
import time
import turtle

from data import config
from data.button import Button
from data.history import History


def generate_number_sequence(items):
    return [
        str(random.randint(0, 9)) for _ in range(items)
    ]


class Manager:
    flick_time = 0.1  # Blank time between numbers
    effective_delay_time = config.DELAY_TIME - flick_time

    font_style = ('Console', 108, 'bold')
    font_style_2 = ('Console', 36, 'normal')
    number_position = (0, -100)
    text_position = (0, 100)
    row_padding = 80

    button_done = Button(text='Done', position=(0, -100), color='black')
    button_close = Button(text='Report & Close', position=(150, -250), color='darkgrey')

    button_success = Button(text='Success', position=(-100, -100), color='darkgreen')
    button_fail = Button(text='Fail', position=(100, -100), color='darkred')

    reports_path = os.path.join(os.getcwd(), 'reports')
    filename_format = '%Y%m%d-%H%M%S'

    def __init__(self, start_level=None):
        # Graphics
        self._init_done = False
        self.screen = None
        self.cursor = None

        self._all_cursors = []

        # Game logic
        self.level = start_level or config.DEFAULT_START_LEVEL
        self.number_sequence = None

        # History
        self.history = History()

    def _init(self):
        self.screen = turtle.Screen()
        self.screen.title('Random number string')
        self.screen.setup(600, 600)

        self.cursor = turtle.Turtle()
        self.cursor.hideturtle()
        self.cursor.speed(0)
        self.cursor.seth(90)
        self.cursor.penup()

        self._all_cursors = [
            self.cursor,
            self.button_done,
            self.button_close,
            self.button_success,
            self.button_fail,
        ]

        for button in self._all_cursors:
            if button == self.cursor:
                continue

            button._init()

        self._init_done = True

    def _clear_screen(self):
        for cursor in self._all_cursors:
            cursor.clear()
            cursor.hideturtle()

    def play_round(self):
        if not self._init_done:
            self._init()

        self.number_sequence = generate_number_sequence(self.level)

        self.render_ready_screen(self.level)
        self.cursor.goto(self.number_position)

        for number in self.number_sequence:
            self.display_number(number)
            time.sleep(self.effective_delay_time)

        self.render_recall_screen()

    def display_number(self, number):
        self._clear_screen()
        time.sleep(self.flick_time)
        self.cursor.write(number, font=self.font_style, align='center')

    def render_ready_screen(self, level):
        self._clear_screen()
        self.cursor.goto(self.text_position)
        self.cursor.write(f'Level: {level}', font=self.font_style_2, align='center')
        time.sleep(3)

    def render_recall_screen(self):
        self._clear_screen()
        self.cursor.goto(self.text_position)
        self.cursor.write('Recall...', font=self.font_style_2, align='center')

        self.button_done.render()
        self.button_done.onclick(self.render_result_screen)

        self.button_close.render()
        self.button_close.onclick(self.close)

    def render_result_screen(self, *args):
        self._clear_screen()
        self.display_numbers()

        self.button_success.render()
        self.button_fail.render()

        self.button_success.onclick(self.round_success)
        self.button_fail.onclick(self.round_fail)

    def display_numbers(self):
        number_of_rows = len(self.number_sequence) // 10 + 1
        current_row = number_of_rows - 1
        row_to_print = []

        for index, number in enumerate(self.number_sequence):
            row_to_print.append(number)

            if ((index + 1) % 10 == 0) or index == len(self.number_sequence) - 1:
                self.cursor.goto(
                    0,
                    self.text_position[1] + (
                            current_row * self.row_padding
                    ),
                )
                self.cursor.write(', '.join(row_to_print), font=self.font_style_2, align='center')
                row_to_print = []
                current_row -= 1

    def round_success(self, *args):
        self.history.add_result(self.level, 'success')
        self.level += config.DELTA_INCREASE
        self.play_round()

    def round_fail(self, *args):
        self.history.add_result(self.level, 'fail')
        self.level -= config.DELTA_DECREASE
        self.play_round()

    def close(self, *args):
        self.history.generate_report()
        self.save_report_to_file()
        self.screen.bye()

    def save_report_to_file(self):
        file_name = f'{self.history.end_time.strftime(self.filename_format)}.json'
        file_path = os.path.join(self.reports_path, file_name)

        with open(file_path, 'w') as json_file:
            json.dump(self.history.report, json_file)
