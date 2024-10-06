import math

import pygame

import constants as c
import frame as f
import sys

from primitives import Pose
from sound_manager import SoundManager
from image_manager import ImageManager
from word_manager import WordManager
import asyncio


class Game:
    def __init__(self):
        pygame.init()
        SoundManager.init()
        ImageManager.init()
        WordManager.init()
        self.small_screen = pygame.Surface(c.WINDOW_SIZE)
        self.screen = pygame.display.set_mode(c.SCALED_WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        pygame.mixer.init()

        self.shake_amp = 0
        self.since_shake = 999
        self.reset()

        pygame.display.set_caption(f"{c.CAPTION}")

        self.main()

    def shake(self, amt=15):
        self.shake_amp = amt
        self.since_shake = 0


    def get_shake_offset(self):
        magnitude = math.cos(self.since_shake * 60) * self.shake_amp
        direction = Pose((1, 1))
        if abs(magnitude) < 1:
            magnitude = 0
        return direction * magnitude

    def reset(self):
        self.score = 0
        self.level = 1
        self.total_words = []
        self.upgrades = []

    def main(self):
        current_frame = f.IntroFrame(self)
        current_frame.load()
        self.clock.tick(60)

        while True:
            dt, events = self.get_events()
            if dt == 0:
                dt = 1/100000
            if dt > 0.05:
                dt = 0.05
            current_frame.update(dt, events)
            current_frame.draw(self.small_screen, self.get_shake_offset().get_position())
            scaled = pygame.transform.scale(self.small_screen, c.SCALED_WINDOW_SIZE)
            self.screen.blit(scaled, (0, 0))
            pygame.display.flip()

            if current_frame.done:
                current_frame = current_frame.next_frame()
                current_frame.load()


    def get_events(self):
        dt = self.clock.tick(c.FRAMERATE)/1000

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4:
                    pygame.display.toggle_fullscreen()

        self.since_shake += dt
        self.shake_amp *= 0.006 ** dt

        return dt, events


if __name__ == "__main__":
    Game()
