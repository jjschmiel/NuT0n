import pygame
from config import LOG_FUNCTION_CALLS, WIDTH

def draw_active_game(WIN, player, platformManager, environment, timer_text, highScore):
    if LOG_FUNCTION_CALLS:
        print('running draw_active_game')
    WIN.fill((0, 0, 0)) # Fill the screen with black

    environment.draw(WIN)  # Draw the walls and floor
    platformManager.draw(WIN)
    player.draw(WIN)
    WIN.blit(timer_text, (WIDTH // 2, 50))
    WIN.blit(highScore, (WIDTH // 6, 50))
    pygame.display.update()  # Update the display