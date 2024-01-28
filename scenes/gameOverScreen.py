import pygame
import sys
from config import WIDTH, HEIGHT

def run_game_over_screen(WIN):
    title_font = pygame.font.Font(None, 70)  # Choose the font for the title
    instruction_font = pygame.font.Font(None, 35)  # Choose the font for the instructions

    title = title_font.render("GAME OVER", True, (255, 255, 255))  # Create the title
    instructions = instruction_font.render("Press SPACE to try again", True, (255, 255, 255))  # Create the instructions

    # Load the image

    #WIN.blit(image, (0, 0))
    WIN.blit(title, ((WIDTH - instructions.get_width()) // 2, HEIGHT // 2 - 170))  # Draw the title

    WIN.blit(instructions, ((WIDTH - instructions.get_width()) // 2, HEIGHT // 2 - 70))  # Draw the instructions

    pygame.display.flip()  # Update the display
    start_ticks = pygame.time.get_ticks()  # Starter tick

    waiting = True
    while waiting:  # Wait for the user to press a key
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # Calculate how many seconds

        if seconds > 3:  # If more than 3 seconds have passed
            print("3 seconds have passed!")

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and seconds > 1:  # This will trigger when a key is released
                waiting = False