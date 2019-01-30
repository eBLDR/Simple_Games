# !!! Needs revision - 2018

import turtle
import random
import math as m
import time

# Constants and initial parameters
ANGLE = 0
POWER = 0
valorsX = []
valorsY = []
G = 10
A, B = 0, 0
SP = 2.5
SP_obj = 3
I = 5


def start_pos():
    global ANGLE, POWER, SP
    ANGLE = 45.
    POWER = 8.
    SP = 2.5
    atlas.clear()
    atlas.hideturtle()
    atlas.penup()
    atlas.goto(-250, -250)
    atlas.setheading(ANGLE)
    atlas.shapesize(1.5, SP)
    atlas.pendown()
    atlas.showturtle()


def new_pos():
    global A, B, SP_obj, I
    I = 5
    obj.hideturtle()
    A = random.randint(-200, 300)
    B = random.randint(-200, 300)
    SP_obj = (random.random()+0.1)*5
    obj.goto(A,B)
    obj.shapesize(SP_obj, SP_obj)
    obj.showturtle()
    start_pos()
    intents()


def exit_():
    screen.bye()


def left():
    global ANGLE
    ANGLE += 5.
    atlas.setheading(ANGLE)


def right():
    global ANGLE
    ANGLE -= 5.
    atlas.setheading(ANGLE)


def more_power():
    global POWER, SP
    if POWER < 15:
        POWER += 0.25
        if SP < 8:
            SP += 0.20
            atlas.shapesize(1.5, SP)


def less_power():
    global POWER, SP
    if POWER > 0.25:
        POWER -= 0.25
        if SP > 0.5:
            SP -= 0.20
            atlas.shapesize(1.5, SP)


def intents():
    global I
    msg.clear()
    msg.pencolor('white')
    msg.goto(-280, 120)
    msg.write(str(I), align='left', font=('Arial', 24, 'normal'))


def victory():
    msg.pencolor('red')
    msg.goto(-100, -280)
    msg.write('VICTORY', align='left', font=('Arial', 32, 'normal'))
    msg.goto(-100, -300)
    msg.pencolor('white')
    msg.write('New game in 5, 4, 3...', align='left', font=('Arial', 12))
    time.sleep(5)


def x(t):
    global ANGLE, POWER, G
    ANGLE_PI = ANGLE * (m.pi/180)
    Px = float(m.cos(ANGLE_PI)*POWER*10)
    x = -250 + (Px*t)
    return x


def y(t):
    global ANGLE, POWER, G
    ANGLE_PI = ANGLE * (m.pi/180)
    Py = float(m.sin(ANGLE_PI)*POWER*10)
    y = -250 + (Py*t) - (G/2) * (t**2)
    return y


"""
Not using time to generate positions.
def f(x):
    global ANGLE,POWER,G
    ANGLE_PI = ANGLE * (m.pi/180)
    Px = float(m.cos(ANGLE_PI)*POWER*10)
    Py = float(m.sin(ANGLE_PI)*POWER*10)
    y = -250 + (Py/Px)*(x+250) - (G/2)*(((x+250)/Px)**2)
    return y
"""    


def fire():
    global SP_obj, A, B, I
    screen.onkey(nothing, 'Return')  # To avoid crashing the game while animation
    screen.onkey(nothing, 'space')
    valorsT = []
    maxim = 30
    minim = 0
    N = 100
    valorsX = []
    valorsY = []
    for j in range(0, N, 1):
        t_j = ((maxim-minim)/(N-1.)*j)+minim
        valorsT.append(t_j)
    valorsT = tuple(valorsT)
    
    for q in valorsT:
        valorsX.append(x(q))
    
    for i in valorsT:
        valorsY.append(y(i))
    
    atlas.penup()
    while True:
        for k in range(0, len(valorsX)-1):
            atlas.goto(valorsX[k], valorsY[k])
            atlas.pendown()
            if A-5-(2*SP_obj) < valorsX[k] < A+5+(2*SP_obj):
                if B-1-(6*SP_obj) < valorsY[k] < B+1+(6*SP_obj):
                    victory()
                    new_pos()
                    break
            if (valorsY[k] <= -400) or (valorsY[k] >= 400) or (valorsX[k] <= -400) or (valorsX[k] >= 400):
                I -= 1
                break
        start_pos()
        break
    intents()
    if I == 0:
        new_pos()
    screen.onkey(fire, 'Return')
    screen.onkey(new_pos, 'space')


def nothing():
    pass


# setting window
screen = turtle.Screen()
screen.bgcolor('black')
screen.setup(650, 650)
screen.title('Custom Angry Birds')

# missile object
atlas = turtle.Turtle()
atlas.color('green')
atlas.pensize('2')
atlas.pencolor('white')
atlas.shape('classic')
atlas.shapesize(1.5, SP)

# target objects
obj = turtle.Turtle()
obj.color('red')
obj.shape('turtle')
obj.penup()

# help display
legend = turtle.Turtle()
legend.hideturtle()
legend.penup()
legend.goto(-315, 240)
legend.pencolor('white')
legend.write('Intro => Fire!\nLeft/Right => Direction\nUp/Down => Power\nSpace => '
             'New Position\nEsc => Exit', align='left')

# messages
msg = turtle.Turtle()
msg.hideturtle()
msg.penup()

# initialisation of the game
start_pos()
new_pos()

# setting keys
screen.onkey(new_pos, 'space')
screen.onkey(exit_, 'Escape')
screen.onkey(fire, 'Return')
screen.onkey(left, 'Left')
screen.onkey(right, 'Right')
screen.onkey(more_power, 'Up')
screen.onkey(less_power, 'Down')


# mainloop
screen.listen()
screen.mainloop()
