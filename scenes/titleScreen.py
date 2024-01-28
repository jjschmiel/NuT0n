import pygame
import sys
from config import WIDTH, HEIGHT

def run_title_screen(WIN):
    title_font = pygame.font.Font(None, 70)  # Choose the font for the title
    instruction_font = pygame.font.Font(None, 35)  # Choose the font for the instructions

    title = title_font.render("My Game", True, (255, 255, 255))  # Create the title
    instructions = instruction_font.render("Press any key to start", True, (255, 255, 255))  # Create the instructions

    # Load the image
    image = pygame.image.load('./Assets/Logo/logo.png')
    image = pygame.transform.scale(image, (WIDTH, 300))  # Resize the image to fit the screen

    WIN.blit(image, (0, HEIGHT // 2 - 150))
    WIN.blit(instructions, ((WIDTH - instructions.get_width()) // 2, HEIGHT - 70))  # Draw the instructions

    pygame.display.flip()  # Update the display

    waiting = True
    while waiting:  # Wait for the user to press a key
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:  # This will trigger when a key is released
                waiting = False