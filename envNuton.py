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

        pygame.init()  # Initialize the pygame module
        pygame.mixer.init()  # Initialize the mixer module
        pygame.mixer.music.load("Assets/Audio/LVL1.ogg")  # Load the music file
        pygame.mixer.music.play()  # Play the music, -1 means loop indefinitely
        self.WIN = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

        def play_lvl2_music():
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

        self._action_spec = array_spec.BoundedArraySpec(
            shape=(2,), dtype=np.int32, minimum=0, maximum=2, name='action')
        
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(1,), dtype=np.int32, minimum=0, name='observation')
        
        # Initialize the clock attribute
        self.clock = pygame.time.Clock()

        self.highScore = 0
    

    def _step(self, action):
        if self.player.alive ==  False:
            return self.reset()

        self.clock.tick(60)  # Cap the frame rate at 60 FPS

        # Calculate how many seconds
        self.seconds = (pygame.time.get_ticks() - self.start_ticks) / 1000

        if self.seconds >= 10 and self.playingLVL2Music == False:
            self.play_lvl2_music()
            self.playingLVL2Music = True

        if self.seconds >= 20 and self.playingLVL3Music == False:
            self.play_lvl3_music()
            self.playingLVL3Music = True

        if self.seconds >= 30 and self.playingLVL4Music == False:
            self.play_lvl4_music()
            self.playingLVL4Music = True

        if self.seconds >= 40 and self.playingBeyondMusic == False:
            self.play_beyond_music()
            self.playingBeyondMusic = True

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

        update_active_game(self.player, self.platformManager, self.environment, self.seconds, self.starManager)
        draw_active_game(self.WIN, self.player, self.platformManager, self.environment, self.timer_text, self.highScore_text, self.starManager)

        #sleep(0)
        if self.player.alive == False:
            return ts.termination(np.array([self._state], dtype=np.int32), reward=-10)
        else:
            return ts.transition(np.array([self._state], dtype=np.int32), reward=1.0)
        
    def _reset(self):
        self._state = 0
        self._episode_ended = False
        print("Running active game")
        self.playingLVL2Music = False
        self.playingLVL3Music = False
        self.playingLVL4Music = False
        self.playingBeyondMusic = False

        pygame.mixer.init()  # Initialize the mixer module
        pygame.mixer.music.load("Assets/Audio/LVL1.ogg")  # Load the music file
        pygame.mixer.music.play()  # Play the music, -1 means loop indefinitely

        def play_lvl2_music():
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
        return ts.restart(np.array([self._state], dtype=np.int32))
    
    def observation_spec(self):
        print("**********in observation_spec***************")
        return self._observation_spec
    
    def action_spec(self):
        print("**********in action_spec***************")
        return self._action_spec
