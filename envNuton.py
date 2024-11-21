from scenes.activeGame.updateActiveGame import update_active_game
from scenes.activeGame.drawActiveGame import draw_active_game
from GameObjects.Player import create_player
from GameObjects.Environment import Environment
from GameObjects.PlatformManager import PlatformManager
from GameObjects.Star import Star
from GameObjects.StarManager import StarManager
import config
import pygame
import sys
import math
from tf_agents.specs import array_spec
from tf_agents.specs import tensor_spec
from tf_agents.environments import py_environment
from tf_agents.trajectories import time_step as ts
import numpy as np
import pymunk
from pygame.color import *
import random

GRAVITY = -200.00

EVADER_DIAMETER = 0

# ___Raycasts___
drawRays = True

# Prevent Raycasts from ending early on evader
RAYCAST_PADDING = 2

# List of ray starting points relative to evader body position
ray_start = [
    [-EVADER_DIAMETER - RAYCAST_PADDING,  RAYCAST_PADDING],
    [-EVADER_DIAMETER + RAYCAST_PADDING, EVADER_DIAMETER - RAYCAST_PADDING],
    [-RAYCAST_PADDING, EVADER_DIAMETER + RAYCAST_PADDING],
    [RAYCAST_PADDING, EVADER_DIAMETER + RAYCAST_PADDING],
    [EVADER_DIAMETER - RAYCAST_PADDING, EVADER_DIAMETER - RAYCAST_PADDING],
    [EVADER_DIAMETER + RAYCAST_PADDING,  RAYCAST_PADDING],
    [EVADER_DIAMETER + RAYCAST_PADDING,  RAYCAST_PADDING],
    [EVADER_DIAMETER + RAYCAST_PADDING,  RAYCAST_PADDING]
]

# List of ray ending points relative to evader body position
ray_end = [
    [400, 400],
    [-400, 400],
    [400, -400],
    [-400, -400],
    [-400, 1],
    [1, 400],
    [400, 1],
    [1, -400]
]



assert len(ray_start) == len(ray_end)
#NUM_RAYS = len(ray_start)
NUM_RAYS = 8

class Nut0nEnv(py_environment.PyEnvironment):
    def __init__(self):
        super().__init__()
        #print("Running active game")
        self.playingLVL2Music = False
        self.playingLVL3Music = False
        self.playingLVL4Music = False
        self.playingBeyondMusic = False
        self.jump_counter = 0

        self.RIGHT_EDGE_OF_PLAY_AREA = config.RIGHT_EDGE_OF_PLAY_AREA
        self.LEFT_EDGE_OF_PLAY_AREA = config.LEFT_EDGE_OF_PLAY_AREA


        pygame.init()  # Initialize the pygame module
        pygame.mixer.init()  # Initialize the mixer module
        #pygame.mixer.music.load("Assets/Audio/LVL1.ogg")  # Load the music file
        #pygame.mixer.music.play()  # Play the music, -1 means loop indefinitely
        self.WIN = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

        self.space = pymunk.Space()
        self.space.gravity = 0.0, GRAVITY
        self.space.damping = 0.8

        # def play_lvl2_music(self):
        #     pygame.mixer.music.load("Assets/Audio/LVL2.ogg")
        #     pygame.mixer.music.play()

        # def play_lvl3_music():
        #     pygame.mixer.music.load("Assets/Audio/LVL3.ogg")
        #     pygame.mixer.music.play()

        # def play_lvl4_music():
        #     pygame.mixer.music.load("Assets/Audio/LVL4.ogg")
        #     pygame.mixer.music.play()

        # def play_beyond_music():
        #     pygame.mixer.music.load("Assets/Audio/BEYOND.ogg")
        #     pygame.mixer.music.play(-1)

        self.environment = Environment()
        self.platformManager = PlatformManager()
        self.starManager = StarManager()

        self.player = create_player()

        self.start_ticks = pygame.time.get_ticks()  # Starter tick

        pygame.font.init()  # Initialize the font module
        self.font = pygame.font.Font(None, 36) # Font for timer

        self.ready_to_increase = True

        self.m_scroll_speed = config.SCROLL_SPEED

        self.star = Star(400, 400)
        
        self.max_platforms = 0
        self.seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000
        
        # Initialize the clock attribute
        self.clock = pygame.time.Clock()

        self.highScore = 0

        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(NUM_RAYS,), dtype=np.float32, minimum=0.0, maximum=99999.9,name='observation')
        
        self._time_step_spec = ts.time_step_spec(self.observation_spec())
        

        self._action_spec = array_spec.BoundedArraySpec(
                shape=(), dtype=np.int32, minimum=0, maximum=1, name='move')
        

        # self._action_spec = {
        #     'move': array_spec.BoundedArraySpec(
        #         shape=(), dtype=np.int32, minimum=0, maximum=2, name='move'),
        #     'jump': array_spec.BoundedArraySpec(
        #         shape=(), dtype=np.int32, minimum=0, maximum=1, name='jump')
        # }

        # self._reward_spec = array_spec.BoundedArraySpec(
        #     shape=(2,), dtype=np.int64, minimum=-100, maximum=100, name='reward')

    def _step(self, action):
        self.reward = 0

        if self.player.alive ==  False:
            return self.reset()
        
        if action == 0:
            self.player.moveRight = False
            self.player.moveLeft = True
        
        if action == 1:
            self.player.moveRight = True
            self.player.moveLeft = False

        # if action['move'] == 2:
        #     self.player.moveRight = False
        #     self.player.moveLeft = True

        # if action['jump'] == 0:
        #     self.player.jump = False

        # if action['jump'] == 1:
        #     self.player.jump = True

        if self.jump_counter < 20:
            self.player.jump = True
            self.jump_counter += 1
        else:
            self.player.jump = False
            self.jump_counter = 0

        self.clock.tick(60)  # Cap the frame rate at 60 FPS

        # Calculate how many seconds
        self.seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000

        # if self.seconds >= 10 and self.playingLVL2Music == False:
        #     self.play_lvl2_music(self)
        #     self.playingLVL2Music = True

        # if self.seconds >= 20 and self.playingLVL3Music == False:
        #     self.play_lvl3_music()
        #     self.playingLVL3Music = True

        # if self.seconds >= 30 and self.playingLVL4Music == False:
        #     self.play_lvl4_music()
        #     self.playingLVL4Music = True

        # if self.seconds >= 40 and self.playingBeyondMusic == False:fo
        #     self.play_beyond_music()
        #     self.playingBeyondMusic = True

        if math.floor(self.seconds) % 10 == 0 and self.ready_to_increase:
            self.m_scroll_speed += 1
            self.ready_to_increase = False
        elif not math.floor(self.seconds) % 10 == 0:
            self.ready_to_increase = True

        self.platformManager.setScrollSpeed(self.m_scroll_speed)
        self.environment.setScrollSpeed(self.m_scroll_speed)
        self.environment.setTime(self.seconds)
        self.starManager.setTime(self.seconds)

        # Render the timer text
        self.timer_text = self.font.render(str(int(self.seconds)), True, (255, 255, 255))
        self.highScore_text = self.font.render("HIGH SCORE: " + str(int(self.highScore)), True, (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        # #REWARDS

        # #Reward for how long you don't die
        # self.reward += self.seconds * 3.0
        
        # #Reward for how high you get
        self.reward += (1000 - self.player.y) * 0.042 

        #Reward for being in the center
        # self.reward -= abs(self.player.x - 960) * 0.06
        
        #Reward for jumping
        # if action['jump'] == 1:
        #     self.reward += 1

        # #Reward for moving
        # if action['move'] == 1:
        #     self.reward += 5

        # if action['move'] == 2:
        #     self.reward += 5

        # #self.reward -= abs(self.player.x - 960) * 0.004

        # for platform in self.platformManager.platforms:
        #     if self.player.y + 50 >= platform.y and self.player.y + 50 <= platform.y + 10:
        #         #print("touching platform")
        #         self.reward += (1000 - platform.y) * 0.0002

        # #print("play y: {0}".format(self.player.y))

        

        update_active_game(self.player, self.platformManager, self.environment, self.seconds, self.starManager)
        draw_active_game(self.WIN, self.player, self.platformManager, self.environment, self.timer_text, self.highScore_text, self.starManager)

        self.alphas = []
        ex = self.player.x
        ey = self.player.y

        for i in range(NUM_RAYS):
            start_x = ex + ray_start[i][0]
            start_y = ey + ray_start[i][1]
            start = start_x, start_y

            end_x = ex + ray_end[i][0]
            end_y = ey + ray_end[i][1]
            end = end_x, end_y

            p1 = int(start_x), int((start_y))
            p2 = int(end_x), int((end_y))
            # pygame.draw.line(self.WIN, THECOLORS["green"], p1, p2, 1)
            # pygame.display.flip()

            # Create a list of all sprites
            all_sprites = self.platformManager.platforms

            ray_sprite = pygame.sprite.Sprite()
            ray_sprite.rect = pygame.Rect(start_x, start_y, end_x - start_x, end_y - start_y)
            collided_sprites = pygame.sprite.spritecollide(ray_sprite, all_sprites, False)

            if collided_sprites:
                collision_point = collided_sprites[0].rect.center
                pygame.draw.line(self.WIN, THECOLORS["red"], p1, collision_point, 1)
                pygame.display.flip()
                collision_point = collided_sprites[0].rect.center
                distance = math.sqrt((collision_point[0] - start_x) ** 2 + (collision_point[1] - start_y) ** 2)
                # print("collision point: {0}".format(collision_point))
                # self.reward += 10 / distance + ((1000 - collision_point[1]) * 0.042)
                self.alphas.append(distance)
            else:
                self.alphas.append(0.0)

        #Penalty for touching the right wall
        if self.player.x + 46 >= self.RIGHT_EDGE_OF_PLAY_AREA:
            self.reward += -10
            # return ts.termination(np.array(self.alphas, dtype=np.float32), reward=self.reward)

        #Penalty for touching the left wall
        if self.player.x - 50 <= self.LEFT_EDGE_OF_PLAY_AREA:
            self.reward += -10
            # return ts.termination(np.array(self.alphas, dtype=np.float32), reward=self.reward)

        #sleep(0)
        if self.player.alive == False:
            #self.reward += -3 + (0.6 * self.seconds)
            #print("Reward: {0}".format(self.reward))
            return ts.termination(np.array(self.alphas, dtype=np.float32), reward=-100)
        else:
            #print("Reward: {0}".format(self.reward))
            #print("aplhass: {0}".format(self.alphas))
            return ts.transition(np.array(self.alphas, dtype=np.float32), reward=self.reward, discount=0.90)
        
    def _reset(self):
        self._state = 0
        self.jump_counter = 0
        self._episode_ended = False
        #print("Running active game")
        self.playingLVL2Music = False
        self.playingLVL3Music = False
        self.playingLVL4Music = False
        self.playingBeyondMusic = False

        pygame.mixer.init()  # Initialize the mixer module
        #pygame.mixer.music.load("Assets/Audio/LVL1.ogg")  # Load the music file
        #pygame.mixer.music.play()  # Play the music, -1 means loop indefinitely

        def play_lvl2_music(self):
            pygame.mixer.music.load("Assets/Audio/LVL2.ogg")
            pygame.mixer.music.play()

        def play_lvl3_music():
            pygame.mixer.music.load("Assets/Audio/LVL3.ogg")
            pygame.mixer.music.play()

        def play_lvl4_music():
            pygame.mixer.music.load("Assets/Audio/LVL4.ogg")
            pygame.mixer.music.play()

        def play_beyond_music():
            pygame.mixer.music.load("Assets/Audio/BEYOND.ogg")
            pygame.mixer.music.play(-1)

        self.environment = Environment()
        self.platformManager = PlatformManager()
        self.starManager = StarManager()

        self.player = create_player()

        self.start_ticks = pygame.time.get_ticks()  # Starter tick

        pygame.font.init()  # Initialize the font module
        self.font = pygame.font.Font(None, 36) # Font for timer

        self.ready_to_increase = True

        self.m_scroll_speed = config.SCROLL_SPEED
        new_obs = []
        for _ in range(NUM_RAYS):
            new_obs.append(1.0)

        self.star = Star(400, 400)
        return ts.restart(np.array(new_obs, dtype=np.float32))
    
    def observation_spec(self):
        #print("**********in observation_spec***************")
        return self._observation_spec
    
    def action_spec(self):
        #print("**********in action_spec***************")
        return self._action_spec
    
    # def reward_spec(self):
    #     #print("**********in action_spec***************")
    #     return self._reward_spec
    
    # def time_step_spec(self):
    #     # print("**********in timee spec***************")
    #     return self._time_step_spec
    