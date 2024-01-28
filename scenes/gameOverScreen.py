import pygame
import sys
from config import WIDTH, HEIGHT

def run_game_over_screen(WIN):
    title_font = pygame.font.Font(None, 70)  # Choose the font for the title
    instruction_font = pygame.font.Font(None, 35)  # Choose the font for the instructions

    title = title_font.render("GAME OVER", True, (255, 255, 255))  # Create the title
    instructions = instruction_font.render("Press any key to try agin", True, (255, 255, 255))  # Create the instructions

    # Load the image

    #WIN.blit(image, (0, 0))
    WIN.blit(title, ((WIDTH - instructions.get_width()) // 2, HEIGHT // 2 - 170))  # Draw the title

    WIN.blit(instructions, ((WIDTH - instructions.get_width()) // 2, HEIGHT // 2 - 70))  # Draw the instructions

    pygame.display.flip()  # Update the display

    waiting = True
    while waiting:  # Wait for the user to press a key
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:  # This will trigger when a key is released
                waiting = False