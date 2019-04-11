import random
import turtle

SCREEN_SIZE = 600
GRID_SIZE = 5


class MyTurtle(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.has_turtle = False

    def reveal(self, x, y):
        if self.has_turtle:
            self.shape('turtle')
            self.color('green')
            self.shapesize(2, 2)
        else:
            self.hideturtle()


class Board:
    def __init__(self):
        self.size = 4
        self.board = []
        self.hidden_turtle_indexes = self.get_hidden_turtle_indexes()

    def get_hidden_turtle_indexes(self):
        return random.randint(0, self.size - 1), random.randint(0, self.size - 1)

    def set_turtle_object(self, i, j):
        t = MyTurtle()
        t.penup()
        t.color('black')
        t.shape('square')
        t.shapesize(3, 3)
        t.speed('fast')
        t.goto(i + 1, j + 1)

        # Bind event
        t.onclick(t.reveal, btn=1)

        # Set hidden turtle
        if (i, j) == self.hidden_turtle_indexes:
            t.has_turtle = True

        return t

    def generate_board(self):
        self.board = [[self.set_turtle_object(i, j) for i in range(self.size)]
                      for j in range(self.size)]

    def run(self):
        self.generate_board()


screen = turtle.Screen()
screen.setup(SCREEN_SIZE, SCREEN_SIZE)
screen.title('Find Turtle!')
screen.setworldcoordinates(0, 0, GRID_SIZE, GRID_SIZE)

board = Board()
board.run()

screen.listen()
screen.mainloop()
