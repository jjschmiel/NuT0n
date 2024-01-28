import pygame
from config import LOG_FUNCTION_CALLS

def draw_active_game(WIN, player, platformManager, environment):
    if LOG_FUNCTION_CALLS:
        print('running draw_active_game')
    WIN.fill((0, 0, 0)) # Fill the screen with black

    environment.draw(WIN)  # Draw the walls and floor
    platformManager.draw(WIN)
    player.draw(WIN)
    pygame.display.update()  # Update the display