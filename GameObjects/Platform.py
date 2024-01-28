import pygame
import random
from config import SMALL_PLATFORM_WIDTH, SMALL_PLATFORM_HEIGHT, SCROLL_SPEED

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()  # Call the Sprite constructor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.y += SCROLL_SPEED


def create_small_platform(x, y):
    return Platform(x, y, SMALL_PLATFORM_WIDTH, SMALL_PLATFORM_HEIGHT, random_platform_img())
    

def random_platform_img():
    return random.choice([
        'Assets/Platform/platform1.png',
        'Assets/Platform/platform2.png',
        'Assets/Platform/platform3.png'
    ])