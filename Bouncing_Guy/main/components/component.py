import abc


class Component(metaclass=abc.ABCMeta):
    
    def __init__(self, **kwargs):
        """
        Builds component object given passed kwargs.
        """
        self.active = kwargs.get('active', True)
        self.render = kwargs.get('render', True)
        self.debug = kwargs.get('debug', False)
        
        # self.width = kwargs.get('width', 0)
        # self.height = kwargs.get('height', 0)
        
        self.x = kwargs.get('x', 0)
        self.y = kwargs.get('y', 0)
    
    @abc.abstractmethod
    def update_self(self):
        pass
    
    @abc.abstractmethod
    def draw_self(self):
        pass
