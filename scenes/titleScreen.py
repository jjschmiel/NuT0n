import pygame
import sys
from config import WIDTH, HEIGHT
import asyncio

async def run_title_screen(WIN):
    pygame.mixer.init()  # Initialize the mixer module
    pygame.mixer.music.load('Assets/Audio/TITLE.ogg')  # Load the music file
    pygame.mixer.music.play(-1)  # Play the music, -1 means loop indefinitely

    instruction_font = pygame.font.Font(None, 35)  # Choose the font for the instructions

    instructions = instruction_font.render("Press any key to start", True, (255, 255, 255))  # Create the instructions

    # Load the image
    image = pygame.image.load('./Assets/Logo/logo.png')
    image = pygame.transform.scale(image, (WIDTH, 300))  # Resize the image to fit the screen

    WIN.blit(image, (0, HEIGHT // 2 - 150))
    WIN.blit(instructions, ((WIDTH - instructions.get_width()) // 2, HEIGHT - 70))  # Draw the instructions

    pygame.display.flip()  # Update the display

    old_win = WIN.copy()  # Save the current state of the window
    #WIN.blit (old_win, (0, 0))  # Draw the old window on top of the current window

    waiting = True
    while waiting:  # Wait for the user to press a key
        pygame.display.flip()  # Update the display
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:  # This will trigger when a key is released
                waiting = False
        await asyncio.sleep(0) 