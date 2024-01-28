import pygame
from scenes.titleScreen import run_title_screen
from scenes.activeGame.runActiveGame import run_active_game
# Set up the environment
# bg_x = 0
#bg = pygame.image.load('background.png')  # Load your background image


def main():
    pygame.init()
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    pygame.mixer.init()  # Initialize the mixer module
    pygame.mixer.music.load('music.mp3')  # Load the music file
    # pygame.mixer.music.play(-1)  # Play the music indefinitely

    run_title_screen(WIN)

    run_active_game(WIN, clock)

if __name__ == "__main__":
    main()