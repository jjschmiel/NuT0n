import pygame
from scenes.titleScreen import run_title_screen
from scenes.activeGame.runActiveGame import run_active_game
from scenes.gameOverScreen import run_game_over_screen
import asyncio
# Set up the environment
# bg_x = 0
#bg = pygame.image.load('background.png')  # Load your background image


async def main():
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    await run_title_screen(WIN)

    highScore = 0

    while True:
        score = await run_active_game(WIN, clock, highScore)
        if score > highScore:
            highScore = score
        await run_game_over_screen(WIN)
        await asyncio.sleep(0) 
        

asyncio.run(main())