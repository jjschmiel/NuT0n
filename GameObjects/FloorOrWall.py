import pygame

class FloorOrWall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.image = pygame.Surface((width, height))
        #self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        
        loaded_image = pygame.image.load(image_path)
        image_width, image_height = loaded_image.get_size()

        for i in range(0, width, image_width):
            for j in range(0, height, image_height):
                self.image.blit(loaded_image, (i, j))