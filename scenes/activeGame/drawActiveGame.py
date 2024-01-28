import pygame
from config import LOG_FUNCTION_CALLS

def draw_active_game(WIN, environment, player):
    if LOG_FUNCTION_CALLS:
        print('running draw_active_game')
    WIN.fill((0, 0, 0)) # Fill the screen with black

    environment.draw(WIN)  # Draw the walls and floor
    player.draw(WIN)
    pygame.display.update()  # Update the display