from config import PLAYER_HEIGHT, PLAYER_WIDTH, HEIGHT, LOG_FUNCTION_CALLS, FLOOR_HEIGHT, WALL_WIDTH, LEFT_EDGE_OF_PLAY_AREA, RIGHT_EDGE_OF_PLAY_AREA


def handle_collisions(player, platforms):
    if LOG_FUNCTION_CALLS:
        print('running handle_collisions')
    #Blocked by walls
    if player.x < LEFT_EDGE_OF_PLAY_AREA + WALL_WIDTH:
        player.x = LEFT_EDGE_OF_PLAY_AREA + WALL_WIDTH
    elif player.x > RIGHT_EDGE_OF_PLAY_AREA - PLAYER_WIDTH:
        player.x = RIGHT_EDGE_OF_PLAY_AREA - PLAYER_WIDTH

    #Blocked by floor
    if player.y > HEIGHT - FLOOR_HEIGHT - PLAYER_HEIGHT:
        player.y = HEIGHT - FLOOR_HEIGHT - PLAYER_HEIGHT
        player.canJump = True
        player.alive = False
        

    for p in platforms:
        handle_platform_collision(player, p)


def handle_platform_collision(player, platform):
    if player.colliderect(platform):
        if player.y < platform.rect.y:  # Player is on the top side of the platform
            player.y = platform.rect.y - PLAYER_HEIGHT
            player.canJump = True
        elif player.y >= platform.rect.y:  # Player is on the bottom side of the platform
            player.y = platform.rect.y + PLAYER_HEIGHT
        elif player.x < platform.rect.x:  # Player is on the left side of the platform
            player.x = platform.rect.x - PLAYER_WIDTH
        elif player.x > platform.rect.x:  # Player is on the right side of the platform
            player.x = platform.rect.x + PLAYER_WIDTH