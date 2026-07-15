import random
import pygame
import object
from functions import lerp

class Inimigo(object.Object):

    def __init__(self, x, y, scale, alpha):

        super().__init__(x, y, scale, alpha)
        self.vspd = -2

        self.add_sprite("images/inimigo_preparando.png")
        self.add_sprite("images/inimigo_atirando.png")
        self.add_sprite("images/inimigo_morto.png")

        self.y_start = y
        self.current_sprite = 0
        self.timer = random.randint(10, 60)
    
    def update(self, dt):
        if self.current_sprite == 0:
            self.y = lerp(self.y, self.y_start, .1)
            self.scale = 1
        elif self.current_sprite == 1:

            self.y = lerp(self.y, self.y_start, .1)
            self.scale = 1
        elif self.current_sprite == 2:

            self.vspd += dt*10
            self.y += self.vspd
            self.scale -= .005

    def draw(self, screen, xoff, yoff, cam_zoom):

        sprite = pygame.transform.scale(self.sprites[self.current_sprite],(max(self.get_width() * cam_zoom * self.scale, 0), max(self.get_height() * cam_zoom * self.scale, 0)))
        screen.blit(sprite, (self.x + xoff - self.get_width()*self.scale*cam_zoom / 2, self.y + yoff - self.get_height()*self.scale*cam_zoom / 2 + cam_zoom * 30))
            
    def die(self):
        self.current_sprite = 2
        self.vspd = -5
        self.scale = 1

    def shoot(self):
        self.current_sprite = 1
        