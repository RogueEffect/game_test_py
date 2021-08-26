
import pygame

# base mob class
class Mob:
    def __init__(self):
        self.rect = pygame.Rect(10.0, 10.0, 64, 64)
        self.color = 0xff00ff
        self.tickcount = 0
    
    def set_size(self, size):
        self.rect.width, self.rect.height = size
    
    def set_pos(self, pos):
        self.rect.x, self.rect.y = pos
    
    def move(self, dx, dy):
        self.rect.move_ip(dx, dy)
    
    def tick(self):
        self.tickcount += 1
    
    def render(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
