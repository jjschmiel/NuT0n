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
from tf_agents.environments import py_environment
from tf_agents.trajectories import time_step as ts
import numpy as np


class Nut0nEnv(py_environment.PyEnvironment):
    def __init__(self):
        super().__init__()
        #print("Running active game")
        self.playingLVL2Music = False
        self.playingLVL3Music = False
        self.playingLVL4Music = False
        self.playingBeyondMusic = False

        self.RIGHT_EDGE_OF_PLAY_AREA = config.RIGHT_EDGE_OF_PLAY_AREA
        self.LEFT_EDGE_OF_PLAY_AREA = config.LEFT_EDGE_OF_PLAY_AREA


        pygame.init()  # Initialize the pygame module
        pygame.mixer.init()  # Initialize the mixer module
        #pygame.mixer.music.load("Assets/Audio/LVL1.ogg")  # Load the music file
        #pygame.mixer.music.play()  # Play the music, -1 means loop indefinitely
        self.WIN = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

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

        self._action_spec = {
            'move': array_spec.BoundedArraySpec(
                shape=(), dtype=np.int32, minimum=0, maximum=2, name='move'),
            'jump': array_spec.BoundedArraySpec(
                shape=(), dtype=np.int32, minimum=0, maximum=1, name='jump')
        }
        
        self.max_platforms = 0
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(self.max_platforms,), dtype=np.float32, minimum=0, name='observation')
        
        # Initialize the clock attribute
        self.clock = pygame.time.Clock()

        self.highScore = 0

        self.reward = 0
    

    def _step(self, action):
        #print("action: {0}".format(action))

        self.reward = 0

        if self.player.alive ==  False:
            return self.reset()
        
        if action['move'] == 1:
            self.player.moveRight = False
            self.player.moveLeft = False
        
        if action['move'] == 0:
            self.player.moveRight = True
            self.player.moveLeft = False

        if action['move'] == 2:
            self.player.moveRight = False
            self.player.moveLeft = True

        if action['jump'] == 0:
            self.player.jump = False

        if action['jump'] == 1:
            self.player.jump = True

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

        # if self.seconds >= 40 and self.playingBeyondMusic == False:
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

        self.reward += self.seconds * -0.6
        self.reward += (1000 - self.player.y) * (1/ 60) # 0.007
        
        if self.player.x + 46 >= self.RIGHT_EDGE_OF_PLAY_AREA:
            self.reward += -1

        if self.player.x - 50 <= self.LEFT_EDGE_OF_PLAY_AREA:
            self.reward += -1

        if action['jump'] == 1:
            self.reward += 1.5

        #self.reward -= abs(self.player.x - 960) * 0.004

        for platform in self.platformManager.platforms:
            if self.player.y + 50 >= platform.y and self.player.y + 50 <= platform.y + 10:
                self.reward += 0.5

        #print("play y: {0}".format(1000 - self.player.y))

        update_active_game(self.player, self.platformManager, self.environment, self.seconds, self.starManager)
        draw_active_game(self.WIN, self.player, self.platformManager, self.environment, self.timer_text, self.highScore_text, self.starManager)

        #sleep(0)
        if self.player.alive == False:
            self.reward += -3 + (0.6 * self.seconds)
            print("Reward: {0}".format(self.reward))
            return ts.termination(observation=self._get_observation(), reward=self.reward)
        else:
            #print("Reward: {0}".format(self.reward))
            return ts.transition(observation=self._get_observation(), reward=self.reward)
        
    def _reset(self):
        self._state = 0
        self._episode_ended = False
        print("Running active game")
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

        self.star = Star(400, 400)
        return ts.restart(observation=self._get_observation())
    
    def observation_spec(self):
        #print("**********in observation_spec***************")
        return self._observation_spec
    
    def action_spec(self):
        #print("**********in action_spec***************")
        return self._action_spec


    def _get_observation(self):
        self.positions = []
        # Get player and platform positions

        #self.positions.append([self.player.x] )

        i = 1

        for platform in self.platformManager.platforms:
              if i < self.max_platforms:
                  self.positions.append([platform.x])
                  i += 1

        # Pad platform positions with NaN if there are fewer than max_platforms
        if len(self.positions) < self.max_platforms:
            padding = [(0, 0)] * (self.max_platforms - len(self.positions))
            self.positions.extend(padding)

        # Create observation dictionary
        observation = {
            #'player_position': np.array(player_pos, dtype=np.float32),
            'positions': np.array(self.positions, dtype=np.float32)
        }
        #print("Observation: {0}".format(observation))

        return observation