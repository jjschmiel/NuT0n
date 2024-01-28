import pygame
from scenes.titleScreen import run_title_screen
from scenes.activeGame.runActiveGame import run_active_game
from scenes.gameOverScreen import run_game_over_screen
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

    while True:
        run_active_game(WIN, clock)
        run_game_over_screen(WIN)

if __name__ == "__main__":
    main()