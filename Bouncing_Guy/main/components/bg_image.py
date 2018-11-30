from pyglet import image, sprite

from main.components.component import Component
from main.settings import config


class Background(Component):
    
    def __init__(self, *args, **kwargs):
        """
        Creates the background sprite.
        """
        
        super(Background, self).__init__(**kwargs)
        
        self.image_file_name = 'background.jpeg'
        
        self.image = image.load(config.resources_path + self.image_file_name)
        self.bg_sprite = sprite.Sprite(self.image, self.x, self.y)
        
    def update_self(self):
        """
        Updates position.
        """
        pass
    
    def draw_self(self):
        """
        Draws sprite to screen.
        """
        self.bg_sprite.draw()
