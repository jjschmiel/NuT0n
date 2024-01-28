from scenes.activeGame.updateActiveGame import update_active_game
from scenes.activeGame.drawActiveGame import draw_active_game
from GameObjects.Player import create_player
from GameObjects.Pattern import create_pattern_1, create_pattern_2
from GameObjects.Environment import Environment
from config import HEIGHT
import pygame
import sys

def run_active_game(WIN, clock, highScore):
    pattern_1 = create_pattern_1(400)
    pattern_2 = create_pattern_2(HEIGHT)

    environment = Environment()
    platforms = [*pattern_2.platforms, *pattern_1.platforms]

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
        update_active_game(player, platforms, environment)
        draw_active_game(WIN, environment, player, timer_text, highScore_text, platforms)

    return seconds
