import pygame
import time
from config import JUMP_VELOCITY, VELOCITY, LOG_FUNCTION_CALLS, LOG_KEY_INPUTS


def active_game_controls(player):
    if LOG_FUNCTION_CALLS:
        print('running active_game_controls')

    player.walking = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        if LOG_KEY_INPUTS:
            print('LEFT')
        player.facingRight = False
        player.walking = True
        player.x -= VELOCITY
    if keys[pygame.K_RIGHT]:
        if LOG_KEY_INPUTS:
            print('RIGHT')
        player.facingRight = True
        player.walking = True
        player.x += VELOCITY
        
    if keys[pygame.K_SPACE]:
        if LOG_KEY_INPUTS:
            print('SPACE')
        if player.jumping:
            if time.time() - player.jumpClock < .25:
                player.y -= JUMP_VELOCITY
        elif player.canJump:
            player.jumping = True
            player.canJump = False
            player.jumpClock = time.time()
    elif player.jumping:
        player.jumping = False