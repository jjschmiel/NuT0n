from GameObjects.FloorOrWall import FloorOrWall
from GameObjects.Panel import Panel
from config import WIDTH, HEIGHT, WALL_WIDTH, WALL_HEIGHT, SCROLL_SPEED, PANEL_HEIGHT

PANEL_SCREEN_HEIGHT_DIFF = HEIGHT - PANEL_HEIGHT

class Environment():
    def __init__(self):
        self.walls = [
            FloorOrWall(WIDTH // 2 - 250, 0,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Platform/platform1.png'),
            FloorOrWall(WIDTH // 2 + 250, 0, WALL_WIDTH, WALL_HEIGHT, 'Assets/Platform/platform1.png'),
            FloorOrWall(WIDTH // 2 - 250, -HEIGHT,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Platform/platform1.png'),
            FloorOrWall(WIDTH // 2 + 250, -HEIGHT, WALL_WIDTH, WALL_HEIGHT, 'Assets/Platform/platform1.png')
        ]
        self.panels = [
            Panel(100, PANEL_SCREEN_HEIGHT_DIFF,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Panels/leftPanel.png'),
            Panel(WIDTH - 575, PANEL_SCREEN_HEIGHT_DIFF,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Panels/rightPanel.png'),
            Panel(100, -PANEL_HEIGHT + PANEL_SCREEN_HEIGHT_DIFF,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Panels/leftPanel.png'),
            Panel(WIDTH - 575, -PANEL_HEIGHT + PANEL_SCREEN_HEIGHT_DIFF,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Panels/rightPanel.png')
        ]
    
    def update(self):
        wall_delete_list = []
        panel_delete_list = []
        for w in self.walls:
            w.rect.y += SCROLL_SPEED
            if w.rect.y > HEIGHT:
                wall_delete_list.append(w)
        for p in self.panels:
            p.y += SCROLL_SPEED
            if p.y > HEIGHT:
                panel_delete_list.append(p)
            if p.y > HEIGHT - PANEL_SCREEN_HEIGHT_DIFF and len(self.panels) < 6:
                self.panels.append(Panel(p.x, -PANEL_HEIGHT + PANEL_SCREEN_HEIGHT_DIFF,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Panels/leftPanel.png'))
        
        for w in wall_delete_list:
            self.walls.append(FloorOrWall(w.rect.x, -HEIGHT,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Platform/platform1.png'))
            self.walls.remove(w)
            del w
        for p in panel_delete_list:
            self.panels.remove(p)
            del p


    def draw(self, WIN):
        for w in self.walls:
            w.draw(WIN)
        for p in self.panels:
            p.draw(WIN)