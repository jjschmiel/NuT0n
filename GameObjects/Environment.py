from GameObjects.FloorOrWall import FloorOrWall
from GameObjects.Panel import Panel
from GameObjects.DeathVoid import DeathVoid
from config import WIDTH, HEIGHT, WALL_WIDTH, WALL_HEIGHT, SCROLL_SPEED, PANEL_HEIGHT
import math

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
        self.deathVoid0 = DeathVoid((WIDTH // 2) - 200, HEIGHT - 50, 450, 50, 'Assets/DeathVoid/deathVoid.gif',0)
        self.deathVoid1 = DeathVoid((WIDTH // 2) - 132, HEIGHT - 50, 450, 50, 'Assets/DeathVoid/deathVoid.gif',2)
        self.deathVoid2 = DeathVoid((WIDTH // 2) - 64, HEIGHT - 50, 450, 50, 'Assets/DeathVoid/deathVoid.gif',4)
        self.deathVoid3 = DeathVoid((WIDTH // 2) + 4 , HEIGHT - 50, 450, 50, 'Assets/DeathVoid/deathVoid.gif',6)
        self.deathVoid4 = DeathVoid((WIDTH // 2) + 72, HEIGHT - 50, 450, 50, 'Assets/DeathVoid/deathVoid.gif',8)
        self.deathVoid5 = DeathVoid((WIDTH // 2) + 140, HEIGHT - 50, 450, 50, 'Assets/DeathVoid/deathVoid.gif',10)
        self.deathVoid6 = DeathVoid((WIDTH // 2) + 208, HEIGHT - 50, 450, 50, 'Assets/DeathVoid/deathVoid.gif',12)
    
    def setScrollSpeed(self, scroll_speed):
        self.scroll_speed = scroll_speed -1

    def setTime(self, time):
        self.time = time

    def update(self):
        self.deathVoid0.update_animation()
        self.deathVoid1.update_animation()
        self.deathVoid2.update_animation()
        self.deathVoid3.update_animation()
        self.deathVoid4.update_animation()
        self.deathVoid5.update_animation()
        self.deathVoid6.update_animation()
        wall_delete_list = []
        panel_delete_list = []
        for w in self.walls:
            w.rect.y += self.scroll_speed
            if w.rect.y > HEIGHT and self.time < 30:
                wall_delete_list.append(w)
        for p in self.panels:
            p.y += self.scroll_speed
            if p.y > HEIGHT and self.time < 20:
                panel_delete_list.append(p)
            if p.y > HEIGHT - PANEL_SCREEN_HEIGHT_DIFF and len(self.panels) < 6 and self.time < 20:
                self.panels.append(Panel(p.x, -PANEL_HEIGHT + PANEL_SCREEN_HEIGHT_DIFF,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Panels/leftPanel.png'))
        
        for w in wall_delete_list:
            self.walls.append(FloorOrWall(w.rect.x, -HEIGHT,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Platform/platform1.png'))
            self.walls.remove(w)
            del w
        for p in panel_delete_list:
            self.panels.remove(p)
            del p
        
        if self.time > 35 and math.floor(self.time) % 2 == 0:
            self.deathVoid0.rect.y +=1
            self.deathVoid1.rect.y +=1
            self.deathVoid2.rect.y +=1
            self.deathVoid3.rect.y +=1
            self.deathVoid4.rect.y +=1
            self.deathVoid5.rect.y +=1
            self.deathVoid6.rect.y +=1



    def draw(self, WIN):
        for w in self.walls:
            w.draw(WIN)
        for p in self.panels:
            p.draw(WIN)
        self.deathVoid0.draw(WIN)
        self.deathVoid1.draw(WIN)
        self.deathVoid2.draw(WIN)
        self.deathVoid3.draw(WIN)
        self.deathVoid4.draw(WIN)
        self.deathVoid5.draw(WIN)
        self.deathVoid6.draw(WIN)