import pygame

death_void_images = [
        pygame.image.load('Assets/DeathVoid/GLOOMBLOOM_000.png'), 
        pygame.image.load('Assets/DeathVoid/GLOOMBLOOM_001.png'),
        pygame.image.load('Assets/DeathVoid/GLOOMBLOOM_002.png'),
        pygame.image.load('Assets/DeathVoid/GLOOMBLOOM_003.png'),
        pygame.image.load('Assets/DeathVoid/GLOOMBLOOM_004.png'),
        pygame.image.load('Assets/DeathVoid/GLOOMBLOOM_005.png'),
        pygame.image.load('Assets/DeathVoid/GLOOMBLOOM_006.png'),
        pygame.image.load('Assets/DeathVoid/GLOOMBLOOM_007.png'),
        pygame.image.load('Assets/DeathVoid/GLOOMBLOOM_008.png'),
        pygame.image.load('Assets/DeathVoid/GLOOMBLOOM_009.png'),
        pygame.image.load('Assets/DeathVoid/GLOOMBLOOM_010.png'),
        pygame.image.load('Assets/DeathVoid/GLOOMBLOOM_011.png'),
        pygame.image.load('Assets/DeathVoid/GLOOMBLOOM_012.png'),
        pygame.image.load('Assets/DeathVoid/GLOOMBLOOM_013.png')
    ]

class DeathVoid(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path, animationCounter):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animationCounter = animationCounter
        self.animationLength = 14
        
        loaded_image = pygame.image.load(image_path)
        image_width, image_height = loaded_image.get_size()

        for i in range(0, width, image_width):
            for j in range(0, height, image_height):
                self.image.blit(loaded_image, (i, j))

    def update_animation(self):
        self.animationCounter += 1
        if self.animationCounter >= self.animationLength:
            self.animationCounter = 0

    def draw(self, window):
        img = death_void_images[self.animationCounter]
        window.blit(img, (self.rect.x, self.rect.y))