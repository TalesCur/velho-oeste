import pygame
from object import Object
import math
from functions import lerp

class Warning(Object):

    def __init__(self, sprite):
        super().__init__(640, 360, 20, 1)
        self.scale_decay = 1
        self.add_sprite("images/ready.png")
        self.add_sprite("images/set.png")
        self.add_sprite("images/go.png")
        self.current_sprite = sprite


    def update(self, dt):
        
        self.keys = pygame.key.get_pressed()
        if self.scale > 3:
            self.scale=lerp(self.scale, .5, .3)
        elif self.scale > 1.2:

            self.scale_decay=lerp(self.scale_decay, .00001, .4)
        else:
            self.scale_decay=lerp(self.scale_decay, 1, .02)
            if self.scale <= 0:

                pass
        
        self.scale -= self.scale_decay
