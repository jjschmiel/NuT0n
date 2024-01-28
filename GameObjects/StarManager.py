import random
from config import WIDTH
from GameObjects.Star import Star

class StarManager():
    def __init__(self):
        self.stars = []

    def setTime(self, time):
        self.time = time

    def update(self):
        if self.time > 2:
            starChance = random.randrange(100)

            if starChance < 10:
                x = random.randrange(WIDTH)
                self.stars.append(Star(x, 0))
        
        for s in self.stars:
            s.update()
    
    def draw(self, WIN):
        for s in self.stars:
            s.draw(WIN)