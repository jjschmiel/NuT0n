import pygame
import sys
import time
from GameObjects.FloorOrWall import FloorOrWall
from GameObjects.Player import Player, create_player, player_images
from GameObjects.Platform import Platform
from GameObjects.Panel import Panel
from config import WIDTH, HEIGHT, VELOCITY, GRAVITY, JUMP_VELOCITY, PLAYER_HEIGHT, PLAYER_WIDTH
from scenes.titleScreen import run_title_screen

# Initialize Pygame
pygame.init()


# set up the display window full screen
WIN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

player = create_player()

# Set up the environment
# bg_x = 0
#bg = pygame.image.load('background.png')  # Load your background image

def draw_window():
    #WIN.blit(bg, (0, 0))  # Draw the background
    pygame.draw.rect(WIN, (255, 0, 0), player)  # Draw the player
    pygame.display.update()  # Update the display

# Define the walls
WALL_WIDTH, WALL_HEIGHT = 50, 1080

# Define the floor
FLOOR_WIDTH, FLOOR_HEIGHT = 550, 50

# Create the walls and floor
floorOrWallImages = [pygame.image.load('Assets/Platform/platform1.png'), pygame.image.load('Assets/Platform/platform2.png'), pygame.image.load('Assets/Platform/platform3.png')]
leftWall = FloorOrWall(WIDTH // 2 - 250, HEIGHT - 1080,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Platform/platform1.png')
rightWall = FloorOrWall(WIDTH // 2 + 250, HEIGHT - 1080, WALL_WIDTH, WALL_HEIGHT, 'Assets/Platform/platform1.png')
floor = FloorOrWall(WIDTH // 2 - 250, HEIGHT - 50, FLOOR_WIDTH, FLOOR_HEIGHT, 'Assets/Platform/platform1.png')
platform = Platform(WIDTH // 2 - 10, HEIGHT - 200, 200, 50, 'Assets/Platform/platform1.png')
platform2 = Platform(WIDTH // 2 - 200, HEIGHT - 300, 200, 50, 'Assets/Platform/platform2.png')
platform3 = Platform(WIDTH // 2 - 20, HEIGHT - 400, 200, 50, 'Assets/Platform/platform3.png')
leftPanel = Panel(100,25,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Panels/leftPanel.png')
rightPanel = Panel(WIDTH - 575, 25,  WALL_WIDTH, WALL_HEIGHT, 'Assets/Panels/rightPanel.png')
environment = pygame.sprite.Group(leftWall, rightWall, floor, platform,platform2, platform3, leftPanel, rightPanel)


def draw_window():
    environment.draw(WIN)  # Draw the walls and floor
    pygame.display.update()  # Update the display

def main():
    clock = pygame.time.Clock()
    jumpClock = time.time()
    jumping = False
    space_pressed = False
    playerAnimationCounter = 0
    playerFacingRight = True  # Add this line before your game loop
    running = True
    
    pygame.mixer.init()  # Initialize the mixer module
    pygame.mixer.music.load('music.mp3')  # Load the music file
    # pygame.mixer.music.play(-1)  # Play the music indefinitely

    run_title_screen(WIN)  # Show the title screen

    running = True
    while running:

        while True:
            clock.tick(60)  # Cap the frame rate at 60 FPS
            WIN.fill((0, 0, 0)) # Fill the screen with black
            platform.draw(WIN)
            platform2.draw(WIN)
            platform3.draw(WIN)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        space_pressed = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        space_pressed = False

            

            player_image = player_images[playerAnimationCounter // 10]
            if not playerFacingRight:
                player_image = pygame.transform.flip(player_image, True, False)
            WIN.blit(player_image, (player.x, player.y))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                playerFacingRight = False
                player.x -= VELOCITY
                playerAnimationCounter = (playerAnimationCounter + 1) % (len(player_images) * 10)
                if player.colliderect(leftWall):
                    player.x += VELOCITY  # Move the player back to the right
                if player.colliderect(rightWall):
                    player.x += VELOCITY # Stop the player from moving
                
            if keys[pygame.K_RIGHT]:
                playerFacingRight = True
                player.x += VELOCITY
                playerAnimationCounter = (playerAnimationCounter + 1) % (len(player_images) * 10)
                if player.colliderect(leftWall):
                    player.x -= VELOCITY  # Move the player back to the left
                    environment.x += VELOCITY
                if player.colliderect(rightWall):
                    player.x -= VELOCITY  # Stop the player from moving
            if keys[pygame.K_SPACE]:
                if not jumping:
                    #print("player.y: " + str(player.y) + " | floor.rect.y: " + str(floor.rect.y))
                    if player.y == floor.rect.y - 64:
                        jumping = True
                        jumpClock = time.time()  # Record the start time of the jump
                    if player.y == platform.rect.y - 64:
                        jumping = True
                        jumpClock = time.time()  # Record the start time of the jump
                    if player.y == platform2.rect.y - 64:
                        jumping = True
                        jumpClock = time.time()  # Record the start time of the jump
                    if player.y == platform3.rect.y - 64:
                        jumping = True
                        jumpClock = time.time()  # Record the start time of the jump
                    if player.y == rightWall.rect.y - 64:
                        jumping = True
                        jumpClock = time.time()  # Record the start time of the jump
                    if player.y == leftWall.rect.y - 64:
                        jumping = True
                        jumpClock = time.time()  # Record the start time of the jump
                if jumping:
                    if time.time() - jumpClock < .25:
                            player.y -= JUMP_VELOCITY
                    elif not space_pressed:
                        jumping = False
                    else:
                        jumping = False

            # Apply gravity
            player.y += GRAVITY

            # Check for collision with the floor
            if player.colliderect(floor):
                player.y = floor.rect.y - 64  # Stop the vertical movement

            if player.colliderect(platform):
                if player.y < platform.rect.y:  # Player is on the bottom side of the platform
                    player.y = platform.rect.y - PLAYER_HEIGHT
                elif player.y >= platform.rect.y:  # Player is on the bottom side of the platform
                    player.y = platform.rect.y + PLAYER_HEIGHT
                elif player.x < platform.rect.x:  # Player is on the left side of the platform
                    player.x = platform.rect.x - PLAYER_WIDTH
                elif player.x > platform.rect.x:  # Player is on the right side of the platform
                    player.x = platform.rect.x + PLAYER_WIDTH

            if player.colliderect(platform2):
                if player.y < platform2.rect.y:  # Player is on the bottom side of the platform
                    player.y = platform2.rect.y - PLAYER_HEIGHT
                elif player.y >= platform2.rect.y:  # Player is on the bottom side of the platform
                    player.y = platform2.rect.y + PLAYER_HEIGHT
                elif player.x < platform2.rect.x:  # Player is on the left side of the platform
                    player.x = platform2.rect.x - PLAYER_WIDTH
                elif player.x > platform2.rect.x:  # Player is on the right side of the platform
                    player.x = platform2.rect.x + PLAYER_WIDTH

            if player.colliderect(platform3):
                if player.y < platform3.rect.y:  # Player is on the bottom side of the platform
                    player.y = platform3.rect.y - PLAYER_HEIGHT
                elif player.y >= platform3.rect.y:  # Player is on the bottom side of the platform
                    player.y = platform3.rect.y + PLAYER_HEIGHT
                elif player.x < platform3.rect.x:  # Player is on the left side of the platform
                    player.x = platform3.rect.x - PLAYER_WIDTH
                elif player.x > platform3.rect.x:  # Player is on the right side of the platform
                    player.x = platform3.rect.x + PLAYER_WIDTH
                

            if player.colliderect(rightWall):
                player.y = rightWall.rect.y - 64  # Stop the vertical movement
            
            if player.colliderect(leftWall):
                player.y = leftWall.rect.y - 64  # Stop the vertical movement

            draw_window()

if __name__ == "__main__":
    main()