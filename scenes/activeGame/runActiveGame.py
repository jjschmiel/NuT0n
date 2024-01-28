from scenes.activeGame.updateActiveGame import update_active_game
from scenes.activeGame.drawActiveGame import draw_active_game
from GameObjects.Player import create_player
from GameObjects.Environment import Environment
from GameObjects.PlatformManager import PlatformManager
import pygame
import sys

def run_active_game(WIN, clock, highScore):


    environment = Environment()
    platformManager = PlatformManager()

    player = create_player()

    start_ticks = pygame.time.get_ticks()  # Starter tick
    font = pygame.font.Font(None, 36) # Font for timer

    while player.alive ==  True:
        clock.tick(60)  # Cap the frame rate at 60 FPS

        # Calculate how many seconds
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000

        # Render the timer text
        timer_text = font.render(str(int(seconds)), True, (255, 255, 255))
        highScore_text = font.render("HIGH SCORE: " + str(int(highScore)), True, (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        update_active_game(player, platformManager, environment)
        draw_active_game(WIN, player, platformManager, environment, timer_text, highScore_text,)

    return seconds
