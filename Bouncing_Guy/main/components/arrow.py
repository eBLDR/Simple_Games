import random

from pyglet import image, sprite

from main.components.component import Component
from main.settings import config


class Arrow(Component):
    
    def __init__(self, *args, **kwargs):
        """
        Creates the arrow's sprite.
        """
        # Starting position
        init_x = config.window_width + config.arrow_width_margin
        init_y = random.randint(config.height_range_min, config.height_range_max)
        kwargs['x'] = init_x
        kwargs['y'] = init_y
        
        super(Arrow, self).__init__(**kwargs)
        
        self.speed = kwargs.get('speed', 1)
        
        self.image_file_name = 'arrow_{}.png'.format(random.randint(1, 9))
        
        self.image = image.load(config.resources_path + self.image_file_name)
        self.width = self.image.width
        self.height = self.image.height
        self.arrow_sprite = sprite.Sprite(self.image, self.x, self.y)
        
        self.out_of_screen = False
    
    def update_self(self):
        """
        Updates position.
        """
        self.x -= self.speed
        
        if self.x < -config.arrow_width_margin:
            self.out_of_screen = True
        
        self.arrow_sprite.set_position(self.x, self.y)
    
    def draw_self(self):
        """
        Draws sprite to screen.
        """
        self.arrow_sprite.draw()
