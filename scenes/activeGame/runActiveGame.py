from scenes.activeGame.updateActiveGame import update_active_game
from scenes.activeGame.drawActiveGame import draw_active_game
from GameObjects.Player import create_player
from GameObjects.Pattern import create_pattern_1, create_pattern_2
from GameObjects.Environment import Environment
from GameObjects.PlatformManager import PlatformManager
from config import HEIGHT
import pygame
import sys

def run_active_game(WIN, clock):
    # pattern_1 = create_pattern_1(400)
    # pattern_2 = create_pattern_2(HEIGHT)

    environment = Environment()
    platformManager = PlatformManager()

    player = create_player()

    while player.alive ==  True:
        clock.tick(60)  # Cap the frame rate at 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        update_active_game(player, platformManager, environment)
        draw_active_game(WIN, player, platformManager, environment)