from GameObjects.Platform import create_small_platform
from config import LEFT_EDGE_OF_PLAY_AREA, RIGHT_EDGE_OF_PLAY_AREA, SMALL_PLATFORM_WIDTH, SMALL_PLATFORM_HEIGHT, WALL_WIDTH


PLAY_AREA_WIDTH = RIGHT_EDGE_OF_PLAY_AREA - LEFT_EDGE_OF_PLAY_AREA
SM_PLAT_RIGHT_WALL_X = PLAY_AREA_WIDTH - SMALL_PLATFORM_WIDTH - WALL_WIDTH

class Pattern():
    def __init__(self, bottom_y):
        self.bottom_y = bottom_y
        self.platforms = []

    def add_platform(self, x, y):
        p = create_small_platform(x + LEFT_EDGE_OF_PLAY_AREA + WALL_WIDTH, -y + self.bottom_y)
        self.platforms.append(p)

    def get_pattern_height(self):
        height = 0
        for p in self.platforms:
            p_top = p.y + SMALL_PLATFORM_HEIGHT
            if p_top > height:
                height = p.top
        return height


def create_pattern_1(bottom_y):
    pattern = Pattern(bottom_y)

    pattern.add_platform(0, 0)
    pattern.add_platform(200, 100)
    pattern.add_platform(SM_PLAT_RIGHT_WALL_X, 0)

    return pattern

def create_pattern_2(bottom_y):
    pattern = Pattern(bottom_y)

    pattern.add_platform(PLAY_AREA_WIDTH // 2 - 10, 200)
    pattern.add_platform(0, 300)
    pattern.add_platform(PLAY_AREA_WIDTH // 2 - 20, 400)

    return pattern

# platform = Platform(WIDTH // 2 - 10, HEIGHT - 200, 200, 50, 'Assets/Platform/platform1.png')
# platform2 = Platform(WIDTH // 2 - 200, HEIGHT - 300, 200, 50, 'Assets/Platform/platform2.png')
# platform3 = Platform(WIDTH // 2 - 20, HEIGHT - 400, 200, 50, 'Assets/Platform/platform3.png')