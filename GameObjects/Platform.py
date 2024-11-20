import pygame
import random
import uuid  # Import the uuid module
from config import SMALL_PLATFORM_WIDTH, SMALL_PLATFORM_HEIGHT
import pymunk

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()  # Call the Sprite constructor
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.id = uuid.uuid4()  # Generate a random UUID
        self.body = pymunk.Body()
        self.shape = pymunk.Poly.create_box(self.body, size=(self.width, self.height))

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, scroll_speed):
        self.rect.y += scroll_speed


def create_small_platform(x, y):
    return Platform(x, y, SMALL_PLATFORM_WIDTH, SMALL_PLATFORM_HEIGHT, random_platform_img())
    

def random_platform_img():
    return random.choice([
        'Assets/Platform/platform1.png',
        'Assets/Platform/platform2.png',
        'Assets/Platform/platform3.png'
    ])