import pygame

import constants as c
import frame as f
import sys
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
        pygame.display.set_caption(c.CAPTION)
        self.clock = pygame.time.Clock()
        pygame.mixer.init()

        self.main()

    def main(self):
        current_frame = f.LevelFrame(self)
        current_frame.load()
        self.clock.tick(60)

        while True:
            dt, events = self.get_events()
            if dt == 0:
                dt = 1/100000
            pygame.display.set_caption(f"{c.CAPTION} ({int(1/dt)} FPS)")
            if dt > 0.05:
                dt = 0.05
            current_frame.update(dt, events)
            current_frame.draw(self.small_screen, (0, 0))
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

        return dt, events


if __name__ == "__main__":
    Game()
