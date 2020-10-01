import datetime
import json
import os
import random
import time
import turtle

# Set up
START_LEVEL = 5
DELTA_INCREASE = 1
DELTA_DECREASE = 2
DELAY_TIME = 1  # In seconds


class History:
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.end_time = None

        self.total_rounds = 0
        self.max_success_level = 0
        self.levels = {}

        self.report = None

    def add_result(self, level, outcome):
        if level not in self.levels:
            self.levels[level] = {
                'success': 0,
                'fail': 0,
                'total': 0,
            }

        self.levels[level][outcome] += 1
        self.levels[level]['total'] += 1
        self.total_rounds += 1

        if level > self.max_success_level:
            self.max_success_level = level

    def calculate_percentages(self):
        for level_stats in self.levels.values():
            level_stats['success_rate'] = round(
                (level_stats['success'] * 100) / level_stats['total'],
                2,
            )

    def generate_report(self):
        self.end_time = datetime.datetime.now()
        self.calculate_percentages()

        self.report = {
            'time': {
                'start': str(self.start_time),
                'end': str(self.end_time),
                'duration': str(self.end_time - self.start_time),
            },
            'total_rounds': self.total_rounds,
            'max_success_level': self.max_success_level,
            'levels': self.levels,
        }


def generate_number_sequence(items):
    number_sequence = []

    for i in range(items):
        number_sequence.append(
            str(random.randint(0, 9)),
        )

    return number_sequence


class Button(turtle.Turtle):
    font_style = ('Console', 24, 'normal')

    def __init__(self, text, position, color):
        super().__init__()
        self.hideturtle()
        self.speed(0)
        self.penup()
        self.shape('square')
        self.shapesize(4, 3)

        self.position = position
        self.text = text
        self.color(color, color)

        self.goto(position)
        self.seth(90)

    def render(self):
        self.forward(30)
        self.write(self.text, font=self.font_style, align='center')
        self.backward(30)
        self.showturtle()


class Manager:
    flick_time = 0.1  # Blank time between numbers
    effective_delay_time = DELAY_TIME - flick_time

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

    def __init__(self):
        # Graphics
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

        # Game logic
        self.level = START_LEVEL
        self.number_sequence = generate_number_sequence(self.level)

        # History
        self.history = History()

    def _clear_screen(self):
        for cursor in self._all_cursors:
            cursor.clear()
            cursor.hideturtle()

    def play_round(self):
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
        self.level += DELTA_INCREASE
        self.play_round()

    def round_fail(self, *args):
        self.history.add_result(self.level, 'fail')
        self.level -= DELTA_DECREASE
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


if __name__ == '__main__':
    manager = Manager()
    manager.play_round()
    manager.screen.listen()
    manager.screen.mainloop()
