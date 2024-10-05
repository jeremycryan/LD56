import pygame
import constants as c
from primitives import Pose
from word_manager import WordManager


class TextPreviewer:

    def __init__(self, position, keyboard):
        self.active = True
        self.current_string = ""
        self.current_string_surf = pygame.Surface((0, 0))
        self.font = pygame.sysfont.SysFont("monospace", 40)
        self.position = Pose(position=position)
        self.since_backspace_held = 0
        self.backspace_held = False
        self.keyboard = keyboard

    def update(self, dt, events):
        if self.active:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    letter = pygame.key.name(event.key).upper()
                    if any([letter in row for row in c.QWERTY_LAYOUT]):
                        self.current_string += letter
                        self.on_current_string_update()
                        continue
                    if event.key == pygame.K_RETURN:
                        self.submit_word()
                    if event.key == pygame.K_BACKSPACE:
                        self.current_string = self.current_string[:-1]
                        self.on_current_string_update()
                        self.since_backspace_held = 0
                        self.backspace_held = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        self.backspace_held = False
                        self.since_backspace_held = 0

            if self.backspace_held:
                self.since_backspace_held += dt
                if self.since_backspace_held > 0.4:
                    self.current_string = self.current_string[:-1]
                    self.on_current_string_update()
                    self.since_backspace_held -= 0.04



    def on_current_string_update(self):
        self.current_string_surf = pygame.Font.render(self.font, self.current_string, True, (255, 0, 0))
        self.keyboard.update_targets(self.current_string)

    def draw(self, surface, offset=(0, 0)):
        x = self.position.x + offset[0] - self.current_string_surf.get_width()//2
        y = self.position.y + offset[1] - self.current_string_surf.get_height()//2
        surface.blit(self.current_string_surf, (x, y))

    def submit_word(self):
        if not WordManager.contains(self.current_string):
            self.on_fail_word()
            return
        self.keyboard.frame.on_word_submission()

    def on_fail_word(self):
        print(f"{self.current_string}... THAT'S NOT A WORD!")

    def reset_word(self):
        self.current_string = ""
        self.on_current_string_update()

