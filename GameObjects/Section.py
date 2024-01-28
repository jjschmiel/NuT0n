# Create the walls and floor
leftWall = FloorOrWall(WIDTH // 2 - 250, HEIGHT - 1080,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Platform/platform1.png')
rightWall = FloorOrWall(WIDTH // 2 + 250, HEIGHT - 1080, WALL_WIDTH, WALL_HEIGHT, 'Assets/Platform/platform1.png')
floor = FloorOrWall(WIDTH // 2 - 250, HEIGHT - 50, FLOOR_WIDTH, FLOOR_HEIGHT, 'Assets/Platform/platform1.png')
platform = Platform(WIDTH // 2 - 10, HEIGHT - 200, 200, 50, 'Assets/Platform/platform1.png')
platform2 = Platform(WIDTH // 2 - 200, HEIGHT - 300, 200, 50, 'Assets/Platform/platform2.png')
platform3 = Platform(WIDTH // 2 - 20, HEIGHT - 400, 200, 50, 'Assets/Platform/platform3.png')
leftPanel = Panel(100,25,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Panels/leftPanel.png')
rightPanel = Panel(WIDTH - 575, 25,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Panels/rightPanel.png')
environment = pygame.sprite.Group(leftWall, rightWall, floor, platform,platform2, platform3, leftPanel, rightPanel)

SECTION_HEIGHT = 500
SECTION_WIDTH = 500
WALL_WIDTH = 50

def create_section():
    leftWall = FloorOrWall(WIDTH // 2 - 250, HEIGHT - 1080,  WALL_WIDTH, SECTION_HEIGHT, 'Assets/Platform/platform1.png')
    rightWall = FloorOrWall(WIDTH // 2 + 250, HEIGHT - 1080, WALL_WIDTH, SECTION_HEIGHT, 'Assets/Platform/platform1.png')