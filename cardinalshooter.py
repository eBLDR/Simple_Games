import turtle as t
from time import sleep
from random import choice, random

# - CONSTANTS -
WIDTH, HEIGHT = 500, 500        # screen size in pixels
SPAWN_BORDER = 10               # enemies spawn n pixels from screen's edge


class Game(object):
    def __init__(self):

        self.playing = True  # control variable

        # - GAME CONFIG -
        self.generation_chance = 0.03        # chances of generating an enemy on each iteration - should be 0.03
        self.speed_increase_every = 10       # every how many enemies destroyed speed increases - should be 10
        self.factor_speed_increase = 1.1     # factor in which speed increases (lapse / factor) - should be 1.1

        # - GAME VARIABLES -
        self.lapse = 0.01                    # initial game speed (lapse between consecutive updates)
        self.destroyed = 0                   # enemies destroyed counter

        # - CONTAINERS -
        self.enemies_e = []  # east
        self.enemies_n = []  # north
        self.enemies_w = []  # west
        self.enemies_s = []  # south
        self.missiles_e = []
        self.missiles_n = []
        self.missiles_w = []
        self.missiles_s = []

    def run(self):
        screen.tracer(0)  # animation off

        if random() < self.generation_chance:
            gen_enemy()

        for e_in_sector, m_in_sector in zip([self.enemies_e, self.enemies_n, self.enemies_s, self.enemies_w],
                                            [self.missiles_e, self.missiles_n, self.missiles_s, self.missiles_w]):
            # moving enemies
            for enemy in e_in_sector:
                enemy.move()

            # check enemy collision with guardian - only the first enemy in the sector
            if len(e_in_sector):
                if check_guardian_collision(e_in_sector[0].xcor(), e_in_sector[0].ycor()):
                    game_over()

            # moving missiles
            for missile in m_in_sector:
                missile.move()

            # check if the first missile of the sector is out of the screen
            if len(m_in_sector):
                if missile_out_of_screen(m_in_sector[0].xcor(), m_in_sector[0].ycor()):
                    m_in_sector[0].hideturtle()
                    m_in_sector.remove(m_in_sector[0])

            # check missile collision with an enemy
            # only the first missile in the sector with the first enemy in the sector
            if len(m_in_sector) and len(e_in_sector):
                if check_missile_collision(m_in_sector[0].xcor(), m_in_sector[0].ycor(),
                                           e_in_sector[0].xcor(), e_in_sector[0].ycor()):

                    e_in_sector[0].hideturtle()
                    e_in_sector.remove(e_in_sector[0])
                    m_in_sector[0].hideturtle()
                    m_in_sector.remove(m_in_sector[0])

                    self.destroyed += 1

                    # increases game's speed if necessary
                    if self.destroyed % self.speed_increase_every == 0:
                        self.lapse /= self.factor_speed_increase

        screen.tracer(1)  # animation on

        # wait before next screen update
        sleep(self.lapse)


class UFO(t.Turtle):
    def __init__(self, angle=0, velocity=0):
        super().__init__()
        self.penup()
        self.setheading(angle)
        self.velocity = velocity

    def move(self):
        self.forward(self.velocity)


class Enemy(UFO):
    def __init__(self, x, y, angle):
        super().__init__(angle=angle, velocity=2)
        self.goto(x, y)


class Missile(UFO):
    def __init__(self, angle):
        super().__init__(angle=angle, velocity=5)
        self.color('blue', 'black')


def game_over():
    screen.clear()
    guardian.write('GAME OVER - DESTROYED: {}'.format(game.destroyed), align='center')
    sleep(1)
    game.playing = False


def gen_enemy():
    screen.tracer(0)
    x, y, angle = init_position()
    direction = 'e' if angle == 180 else 'n' if angle == 270 else 'w' if angle == 0 else 's'
    exec('game.enemies_{}.append(Enemy(x, y, angle))'.format(direction))
    screen.tracer(1)


def init_position():
    pos = ((int(WIDTH / 2) - SPAWN_BORDER, 0, 180),
           (-int(WIDTH / 2) + SPAWN_BORDER, 0, 0),
           (0, int(HEIGHT / 2) - SPAWN_BORDER, 270),
           (0, -int(WIDTH / 2) + SPAWN_BORDER, 90))

    return choice(pos)


def gen_missile(angle):
    screen.tracer(0)
    direction = 'e' if angle == 0 else 'n' if angle == 90 else 'w' if angle == 180 else 's'
    exec('game.missiles_{}.append(Missile(angle))'.format(direction))
    screen.tracer(1)


def shoot_right():
    gen_missile(0)


def shoot_up():
    gen_missile(90)


def shoot_left():
    gen_missile(180)


def shoot_down():
    gen_missile(270)


def check_guardian_collision(x, y):
    gir = 5  # guardian_impact_radius
    return True if -gir <= x <= gir and -gir <= y <= gir else False


def check_missile_collision(mX, mY, eX, eY):
    roi = 3  # radius_of_impact
    return True if (mX - roi) <= eX <= (mX + roi) and (mY - roi) <= eY <= (mY + roi) else False


def missile_out_of_screen(x, y):
    return True if x > (WIDTH / 2) or x < -(WIDTH / 2) or y > (HEIGHT / 2) or y < -(HEIGHT / 2) else False


# Game Object
game = Game()

# Screen Object
screen = t.Screen()
screen.setup(WIDTH, HEIGHT, 100, 100)
screen.title('Cardinal Shooter')

# Guardian Object
guardian = t.Turtle()
guardian.shape('circle')

# - EVENTS -
screen.onkeyrelease(game_over, 'Escape')
screen.onkeyrelease(shoot_right, 'Right')
screen.onkeyrelease(shoot_up, 'Up')
screen.onkeyrelease(shoot_left, 'Left')
screen.onkeyrelease(shoot_down, 'Down')

# collect key events
screen.listen()

# preparation time
sleep(2)

if __name__ == '__main__':
    # - MAIN LOOP -
    while game.playing:
        game.run()

    else:  # end of game
        screen.exitonclick()
