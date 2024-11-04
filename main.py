import pygame
from scenes.titleScreen import run_title_screen
from scenes.activeGame.runActiveGame import run_active_game
from scenes.gameOverScreen import run_game_over_screen
import asyncio
# Set up the environment
# bg_x = 0
# bg = pygame.image.load('background.png')  # Load your background image


def main(skipTitle, nutonEnv=None):
    print("Running main")
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

    if not skipTitle:
        run_title_screen(WIN)

    highScore = 0

    while True:
        score = run_active_game(WIN, clock, highScore, nutonEnv)
        if score > highScore:
            highScore = score
        run_game_over_screen(WIN)
        #sleep(0) 

if __name__ == "__main__":
    main(skipTitle=False)

