from GameObjects.Platform import create_small_platform
from config import LEFT_EDGE_OF_PLAY_AREA, RIGHT_EDGE_OF_PLAY_AREA, SMALL_PLATFORM_WIDTH, WALL_WIDTH

# platform = Platform(WIDTH // 2 - 10, HEIGHT - 200, 200, 50, 'Assets/Platform/platform1.png')
# platform2 = Platform(WIDTH // 2 - 200, HEIGHT - 300, 200, 50, 'Assets/Platform/platform2.png')
# platform3 = Platform(WIDTH // 2 - 20, HEIGHT - 400, 200, 50, 'Assets/Platform/platform3.png')

PLAY_AREA_WIDTH = RIGHT_EDGE_OF_PLAY_AREA - LEFT_EDGE_OF_PLAY_AREA
SM_PLAT_RIGHT_WALL_X = PLAY_AREA_WIDTH - SMALL_PLATFORM_WIDTH - WALL_WIDTH

class Pattern():
    def __init__(self, bottom_y):
        self.bottom_y = bottom_y
        self.platforms = []

    def add_platform(self, x, y):
        p = create_small_platform(x + LEFT_EDGE_OF_PLAY_AREA + WALL_WIDTH, y + self.bottom_y)
        self.platforms.append(p)

def create_pattern_1(bottom_y):
    pattern = Pattern(bottom_y)

    pattern.add_platform(0, 0)
    pattern.add_platform(200, 100)
    pattern.add_platform(SM_PLAT_RIGHT_WALL_X, 0)

    return pattern