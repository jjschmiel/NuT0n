import pygame
import time
from config import HEIGHT, WIDTH, PLAYER_HEIGHT, PLAYER_WIDTH, SCROLL_SPEED


player_images = [
        pygame.image.load('Assets/PlayerAnimation/player1.png'),  
        pygame.image.load('Assets/PlayerAnimation/player2.png'),
        pygame.image.load('Assets/PlayerAnimation/player3.png')
    ]


class Player(pygame.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.vy = 0
        self.facingRight = True
        self.animationCounter = 0
        self.animationLength = 30
        self.jumping = False
        self.canJump = True
        self.jumpClock = time.time()
        self.walking = False
        self.alive = True
    

    def update_animation(self):
        if self.walking:
            self.animationCounter += 1
            if self.animationCounter >= self.animationLength:
                self.animationCounter = 0
        else:
            self.animationCounter = 20

    def draw(self, WIN):
        img = player_images[self.animationCounter // 10]
        
        if not self.facingRight:
            img = pygame.transform.flip(img, True, False)
        
        WIN.blit(img, (self.x, self.y))
    
    def update(self):
        self.y -= SCROLL_SPEED
        

def create_player():
    return Player(WIDTH // 2, HEIGHT - 450, PLAYER_WIDTH, PLAYER_HEIGHT)