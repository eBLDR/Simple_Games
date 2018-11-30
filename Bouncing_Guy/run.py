import random
import sys

import pyglet

from main.settings import config
from main.components.pj import PJ
from main.components.arrow import Arrow
from main.components.bg_image import Background


class Game:
    
    def __init__(self):
        # Components container
        self.components_container = []
        
        self.bg = Background()
        
        self.pj = PJ()
    
    def init(self):
        self.components_container.append(self.pj)
    
    def generate_arrow(self):
        speed = random.randint(config.arrow_speed_range[0], config.arrow_speed_range[1])
        self.components_container.append(Arrow(speed=speed))


# Window's origin coordinates (0, 0) start at the bottom left
window = pyglet.window.Window(height=config.window_height, width=config.window_width)


@window.event
def on_draw():
    """
    Overriding the method, renders the window.
    """
    # Clears the screen
    window.clear()
    
    game.bg.draw_self()
    
    # Label object, @anchor_x/y is the center point
    # level_label = pyglet.text.Label(text="Jumps: {}".format(game.pj.jumps), x=10, y=10)
    # level_label.draw()
    
    # Draw components
    for component in game.components_container:
        component.draw_self()


def update(time):
    """
    Updates our list of components objects.
    :param time: passed by schedule_interval
    """
    if random.uniform(0, 1) < config.arrow_generation_chance:
        game.generate_arrow()
    
    to_be_deleted = []
    
    for component in game.components_container:
        component.update_self()
        if isinstance(component, Arrow) and component.out_of_screen:
            to_be_deleted.append(component)
    
    if to_be_deleted:
        for component in to_be_deleted:
            game.components_container.remove(component)


@window.event
def on_key_press(symbol, modifiers):
    """ Control key press events. """
    if symbol == pyglet.window.key.UP:
        game.pj.up()
    
    if symbol == pyglet.window.key.DOWN:
        game.pj.down()


@window.event
def on_key_release(symbol, modifiers):
    """ Control key release events. """
    if symbol == pyglet.window.key.ESCAPE:
        sys.exit()


def main():
    """ Main method, it contains an embedded method that calls on_draw() function. """
    pyglet.clock.schedule_interval(update, 1 / config.fps)
    
    # Run main loop
    pyglet.app.run()


if __name__ == '__main__':
    game = Game()
    game.init()
    main()
