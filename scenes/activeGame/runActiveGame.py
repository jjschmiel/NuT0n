from scenes.activeGame.updateActiveGame import update_active_game
from scenes.activeGame.drawActiveGame import draw_active_game
from GameObjects.Player import create_player
from GameObjects.FloorOrWall import FloorOrWall
from GameObjects.Platform import Platform
from GameObjects.Panel import Panel
from GameObjects.Pattern import create_pattern_1
from config import WIDTH, HEIGHT, WALL_WIDTH, WALL_HEIGHT, FLOOR_WIDTH, FLOOR_HEIGHT
from GameObjects.Environment import Environment
import pygame
import sys

def run_active_game(WIN, clock):
    # Create the walls and floor
    leftWall = FloorOrWall(WIDTH // 2 - 250, HEIGHT - 1080,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Platform/platform1.png')
    rightWall = FloorOrWall(WIDTH // 2 + 250, HEIGHT - 1080, WALL_WIDTH, WALL_HEIGHT, 'Assets/Platform/platform1.png')
    platform = Platform(WIDTH // 2 - 10, HEIGHT - 200, 200, 50, 'Assets/Platform/platform1.png')
    platform2 = Platform(WIDTH // 2 - 200, HEIGHT - 300, 200, 50, 'Assets/Platform/platform2.png')
    platform3 = Platform(WIDTH // 2 - 20, HEIGHT - 400, 200, 50, 'Assets/Platform/platform3.png')
    leftPanel = Panel(100,25,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Panels/leftPanel.png')
    rightPanel = Panel(WIDTH - 575, 25,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Panels/rightPanel.png')

    pattern_1 = create_pattern_1(400)

    environment = Environment()
    platforms = [platform, platform2, platform3, *pattern_1.platforms]

    player = create_player()
 
    while True:
        clock.tick(60)  # Cap the frame rate at 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
        update_active_game(player, platforms, environment)
        draw_active_game(WIN, environment, player)