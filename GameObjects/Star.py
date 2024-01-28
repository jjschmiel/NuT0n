import pygame
import random

class Star():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.radius = random.randrange(1, 4)

    def draw(self, WIN):
        pygame.draw.circle(WIN, 'white', (self.x, self.y), self.radius)

    def update(self):
        self.y += self.radius
    