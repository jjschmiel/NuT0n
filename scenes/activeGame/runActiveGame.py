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
def run_active_game(WIN, clock, highScore):
    playingLVL2Music = False
    playingLVL3Music = False
    playingLVL4Music = False
    playingBeyondMusic = False

    pygame.mixer.init()  # Initialize the mixer module
    pygame.mixer.music.load("Assets/Audio/LVL1.ogg")  # Load the music file
    pygame.mixer.music.play()  # Play the music, -1 means loop indefinitely

    def play_lvl2_music():
        pygame.mixer.init()
        pygame.mixer.music.load("Assets/Audio/LVL2.ogg")
        pygame.mixer.music.play()
        pygame.mixer.music.set_pos(10)

    def play_lvl3_music():
        pygame.mixer.init()
        pygame.mixer.music.load("Assets/Audio/LVL3.ogg")
        pygame.mixer.music.play()
        pygame.mixer.music.set_pos(20)

    def play_lvl4_music():
        pygame.mixer.init()
        pygame.mixer.music.load("Assets/Audio/LVL4.ogg")
        pygame.mixer.music.play()
        pygame.mixer.music.set_pos(30)

    def play_beyond_music():
        pygame.mixer.init()
        pygame.mixer.music.load("Assets/Audio/BEYOND.ogg")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_pos(40)

    environment = Environment()
    platformManager = PlatformManager()
    starManager = StarManager()

    player = create_player()

    start_ticks = pygame.time.get_ticks()  # Starter tick
    font = pygame.font.Font(None, 36) # Font for timer

    ready_to_increase = True

    m_scroll_speed = config.SCROLL_SPEED

    star = Star(400, 400)
    while player.alive ==  True:
        clock.tick(60)  # Cap the frame rate at 60 FPS

        # Calculate how many seconds
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000

        if seconds >= 10 and playingLVL2Music == False:
            play_lvl2_music()
            playingLVL2Music = True

        if seconds >= 20 and playingLVL3Music == False:
            play_lvl3_music()
            playingLVL3Music = True

        if seconds >= 30 and playingLVL4Music == False:
            play_lvl4_music()
            playingLVL4Music = True

        if seconds >= 40 and playingBeyondMusic == False:
            play_beyond_music()
            playingBeyondMusic = True

        if math.floor(seconds) % 10 == 0 and ready_to_increase:
            m_scroll_speed += 1
            ready_to_increase = False
        elif not math.floor(seconds) % 10 == 0:
            ready_to_increase = True

        platformManager.setScrollSpeed(m_scroll_speed)
        environment.setScrollSpeed(m_scroll_speed)
        environment.setTime(seconds)
        starManager.setTime(seconds)

        # Render the timer text
        timer_text = font.render(str(int(seconds)), True, (255, 255, 255))
        highScore_text = font.render("HIGH SCORE: " + str(int(highScore)), True, (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        update_active_game(player, platformManager, environment, seconds, starManager)
        draw_active_game(WIN, player, platformManager, environment, timer_text, highScore_text, starManager)
        

    return seconds
