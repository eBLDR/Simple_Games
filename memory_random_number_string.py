import random
import time
import turtle

# Set up
START_LEVEL = 5
DELTA_INCREASE = 1
DELTA_DECREASE = 2
DELAY_TIME = 1  # In seconds


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

    button_done = Button(text='Done', position=(0, -100), color='black')
    button_success = Button(text='Success', position=(-100, -100), color='darkgreen')
    button_fail = Button(text='Fail', position=(100, -100), color='darkred')

    def __init__(self):
        # Graphics
        self.screen = turtle.Screen()
        self.screen.title('Random number string')
        self.screen.setup(600, 600)

        self.cursor = turtle.Turtle()
        self.cursor.hideturtle()
        self.cursor.speed(0)
        self.cursor.penup()

        self._all_cursors = [
            self.cursor,
            self.button_done,
            self.button_success,
            self.button_fail,
        ]

        # Game logic
        self.level = START_LEVEL
        self.number_sequence = generate_number_sequence(self.level)

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
        self.cursor.write('Recall', font=self.font_style_2, align='center')

        self.button_done.render()
        self.button_done.onclick(self.render_result_screen)

    def render_result_screen(self, *args):
        self._clear_screen()
        self.display_numbers()

        self.button_success.render()
        self.button_fail.render()

        self.button_success.onclick(self.round_success)
        self.button_fail.onclick(self.round_fail)

    def display_numbers(self):
        # TODO: adjust size and position based on the amount of numbers
        numbers = ', '.join(self.number_sequence)
        self.cursor.write(numbers, font=self.font_style_2, align='center')

    def round_success(self, *args):
        self.level += DELTA_INCREASE
        self.play_round()

    def round_fail(self, *args):
        self.level -= DELTA_DECREASE
        self.play_round()


if __name__ == '__main__':
    manager = Manager()
    manager.play_round()
    turtle.done()
