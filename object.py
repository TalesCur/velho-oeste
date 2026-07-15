import pygame
class Object:

    def __init__(self, x, y, scale, alpha):
        
        self.x = x
        self.y = y
        self.current_sprite = 0
        self.sprites = []
        self.scale = scale
        self.alpha = alpha

    def add_sprite(self, path):
        self.sprites.append(pygame.image.load(path))

    def get_sprite(self):
        if len(self.sprites) > 0:

            return self.current_sprite
        else:

            return 0
        
    def get_width(self):
        if len(self.sprites) > 0:

            return self.sprites[self.current_sprite].get_width()
        else:

            return 0
    
    def get_height(self):

        if len(self.sprites) > 0:

            return self.sprites[self.current_sprite].get_height()
        else:

            return 0
        
    def draw(self, screen):

        if self.scale > 0:

            sprite = pygame.transform.scale(self.sprites[self.current_sprite],(round(self.get_width() * self.scale), round(self.get_height() * self.scale)))
            screen.blit(sprite, (self.x - self.get_width()*self.scale / 2, self.y - self.get_height()*self.scale / 2))