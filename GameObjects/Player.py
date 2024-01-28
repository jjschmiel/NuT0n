import pygame
from config import HEIGHT, WIDTH


class Player(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.vy = 0


def create_player():
    PLAYER_WIDTH = 46
    PLAYER_HEIGHT = 64
    PLAYER_STARTING_POSITION_X_AXIS = WIDTH // 2
    PLAYER_STARTING_POSITION_Y_AXIS = 440

    return Player(WIDTH // 2, HEIGHT - 50, PLAYER_WIDTH, PLAYER_HEIGHT)


player_images = [pygame.image.load('Assets/PlayerAnimation/player1.png'), pygame.image.load('Assets/PlayerAnimation/player2.png'), pygame.image.load('Assets/PlayerAnimation/player3.png')]