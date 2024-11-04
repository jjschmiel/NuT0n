import random 
from GameObjects.Platform import create_small_platform
from config import LEFT_EDGE_OF_PLAY_AREA, RIGHT_EDGE_OF_PLAY_AREA, SMALL_PLATFORM_WIDTH, SMALL_PLATFORM_HEIGHT, WALL_WIDTH, HEIGHT


PLAY_AREA_WIDTH = RIGHT_EDGE_OF_PLAY_AREA - LEFT_EDGE_OF_PLAY_AREA
SM_PLAT_RIGHT_WALL_X = PLAY_AREA_WIDTH - SMALL_PLATFORM_WIDTH - WALL_WIDTH

class PlatformManager():
    def add_platform(self, x, y):
        p = create_small_platform(x + LEFT_EDGE_OF_PLAY_AREA + WALL_WIDTH, -y)
        self.platforms.append(p)

    def create_pattern_1(self):
        self.add_platform(100, 0)
        self.add_platform(200, 100)
        self.add_platform(SM_PLAT_RIGHT_WALL_X, 0)
        self.add_platform(400, 300)

    def create_pattern_2(self):
        self.add_platform(PLAY_AREA_WIDTH // 2 - 10, 0)
        self.add_platform(0, 100)
        self.add_platform(PLAY_AREA_WIDTH // 2 - 20, 400)

    def setScrollSpeed(self, scroll_speed):
        self.scroll_speed = scroll_speed

    def __init__(self):
        self.platforms = []
        self.pattern_makers = [
            self.create_pattern_1,
            self.create_pattern_2
        ]

        self.add_platform(0, -HEIGHT + 200)
        self.add_platform(200, -HEIGHT + 300)
        self.add_platform(SM_PLAT_RIGHT_WALL_X, -HEIGHT + 200)

        self.add_platform(SM_PLAT_RIGHT_WALL_X, -HEIGHT + 400)
        self.add_platform(PLAY_AREA_WIDTH // 2 - 20, -HEIGHT + 600)
        self.add_platform(0, -HEIGHT + 800)

    def update(self):
        platforms = self.platforms
        platforms_to_remove = []
        need_new_platforms = True
        for p in platforms:
            if p.rect.y < 100:
                need_new_platforms = False
        
        if need_new_platforms:
            random.choice(self.pattern_makers)()

        for p in platforms:
            p.update(self.scroll_speed)
            if p.rect.y > HEIGHT:
                platforms_to_remove.append(p)
        
        for p in platforms_to_remove:
            platforms.remove(p)
            del p

    def draw(self, WIN):
        for p in self.platforms:
            #print(f"ID: {p.id  } | x: {p.rect.x} | y: {p.rect.y}")
            p.draw(WIN)