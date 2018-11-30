from pyglet import image, sprite

from main.components.component import Component
from main.settings import config


class PJ(Component):
    
    def __init__(self, *args, **kwargs):
        """
        Creates the PJ's sprite.
        """
        # Starting position
        self.base_x = 240
        self.base_y = 240
        
        kwargs['x'] = self.base_x
        kwargs['y'] = self.base_y
        
        super(PJ, self).__init__(**kwargs)
        
        self.image = image.load(config.resources_path + 'pj.png')
        self.width = self.image.width
        self.height = self.image.height
        self.pj_sprite = sprite.Sprite(self.image, self.x, self.y)
    
    def update_self(self):
        """
        Updates position.
        """

        self.pj_sprite.set_position(self.x, self.y)
    
    def draw_self(self):
        """
        Draws sprite to screen.
        """
        self.pj_sprite.draw()
    
    def up(self):
        """
        Up motion.
        """
        if self.y < config.height_range_max:
            self.y += config.pj_move
    
    def down(self):
        """
        Down motion.
        """
        if self.y > config.height_range_min:
            self.y -= config.pj_move
