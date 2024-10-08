import pygame
import sys
import asyncio
from config import WIDTH, HEIGHT

async def run_game_over_screen(WIN):
    pygame.mixer.init()  # Initialize the mixer module
    pygame.mixer.music.load('Assets/Audio/LOSE.ogg')  # Load the music file
    pygame.mixer.music.play(-1)  # Play the music, -1 means loop indefinitely
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and seconds > 1:  # This will trigger when a key is released
                waiting = False
        await asyncio.sleep(0) 