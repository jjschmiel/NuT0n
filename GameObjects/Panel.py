import pygame
from config import SCROLL_SPEED

class Panel(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()  # Call the Sprite constructor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def update(self):
        self.rect.y += SCROLL_SPEED