from turtle import Turtle


class Button(Turtle):
    font_style = ('Console', 24, 'normal')

    def __init__(self, text, position, color):
        self.position = position
        self.text = text
        self.color_string = color

    def _init(self):
        super().__init__()
        self.hideturtle()
        self.speed(0)
        self.penup()
        self.shape('square')
        self.shapesize(4, 3)
        self.color(self.color_string, self.color_string)

        self.goto(self.position)
        self.seth(90)

    def render(self):
        self.forward(30)
        self.write(self.text, font=self.font_style, align='center')
        self.backward(30)
        self.showturtle()
