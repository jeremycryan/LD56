import math
import random

import pygame
import constants as c
from image_manager import ImageManager
from particle import TextToast
from primitives import Pose
from sound_manager import SoundManager
from word_manager import WordManager


class TextPreviewer:

    def __init__(self, position, keyboard):
        self.active = True
        self.current_string = ""
        self.current_string_surf = pygame.Surface((0, 0))
        self.font = pygame.font.Font("assets/fonts/a_goblin_appears.ttf", 25)
        self.position = Pose(position=position)
        self.since_backspace_held = 0
        self.backspace_held = False
        self.keyboard = keyboard
        self.max_word_length = 5

        self.backdrop = ImageManager.load("assets/images/word_previewer.png")

        self.help_font = pygame.font.Font("assets/fonts/a_goblin_appears.ttf", 8)
        self.on_max_string_change()

        self.since_time_start = 0
        self.max_time_multiplier = 2.0
        self.timer_duration = 18
        self.free_time = 2
        self.timer_is_empty = False

        self.key_sounds = [SoundManager.load(f"assets/audio/key_{i}.ogg") for i in range(1, 5)]


    def update(self, dt, events):
        if self.active:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    letter = pygame.key.name(event.key).upper()
                    if any([letter in row for row in c.QWERTY_LAYOUT]) and len(self.current_string) < self.max_word_length:
                        self.current_string += letter
                        self.on_current_string_update()
                        random.choice(self.key_sounds).play()
                        continue
                    if event.key == pygame.K_RETURN:
                        self.submit_word()
                        random.choice(self.key_sounds).play()
                    if event.key == pygame.K_BACKSPACE:
                        self.current_string = self.current_string[:-1]
                        self.on_current_string_update()
                        self.since_backspace_held = 0
                        self.backspace_held = True
                        random.choice(self.key_sounds).play()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        self.backspace_held = False
                        self.since_backspace_held = 0

            if self.backspace_held:
                self.since_backspace_held += dt
                if self.since_backspace_held > 0.4:
                    if self.current_string:
                        random.choice(self.key_sounds).play()
                        self.current_string = self.current_string[:-1]
                        self.on_current_string_update()
                    self.since_backspace_held -= 0.04
            self.since_time_start += dt


    def on_max_string_change(self):
        self.max_string_surface = self.help_font.render(f"Maximum {self.max_word_length} letters", False, (40, 175, 65))


    def on_current_string_update(self):
        self.current_string_surf = pygame.Font.render(self.font, self.current_string, False, (49, 217, 93))
        self.keyboard.update_targets(self.current_string)

    def draw(self, surface, offset=(0, 0)):
        x = self.position.x + offset[0]
        y = self.position.y + offset[1]
        surface.blit(self.backdrop, (x - self.backdrop.get_width()//2, y - self.backdrop.get_height()//2))
        surface.blit(self.current_string_surf, (x - self.current_string_surf.get_width()//2, y - self.current_string_surf.get_height()//2 - 10))
        surface.blit(self.max_string_surface, (x - self.max_string_surface.get_width()//2, y - self.max_string_surface.get_height()//2 + 13))

        width = (self.calculate_time_multiplier() - 1)**1.4 * 80
        height = 3
        pygame.draw.rect(surface, (40, 175, 65), (x + 70, y + 12, width, height))
        pygame.draw.rect(surface, (40, 175, 65), (x - 70 - width, y + 12, width, height))


    def calculate_time_multiplier(self):
        self.max_time_multiplier = 2.0
        if self.since_time_start < self.free_time:
            return self.max_time_multiplier
        elif self.since_time_start < self.free_time + self.timer_duration:
            return 1 + (self.max_time_multiplier - 1) * (self.timer_duration - (self.since_time_start - self.free_time)) / (self.timer_duration)
        else:
            if not self.timer_is_empty:
                self.keyboard.frame.particles.append(
                    TextToast((self.position + Pose((0, 15))).get_position(), f"NO SPEED BONUS", font_size=10, color=(255, 100, 255)))
                self.timer_is_empty = True
            return 1

    def submit_word(self):
        if not WordManager.contains(self.current_string):
            self.on_fail_word()
            return
        self.keyboard.frame.on_word_submission()
        if self.calculate_time_multiplier() > 1:
            mult = round(self.calculate_time_multiplier(), 1)
            self.keyboard.frame.particles.append(TextToast(self.position.get_position(), f"x{mult}", (255, 255, 0)))
            bonus_position = self.position + Pose((0, 18))
            self.keyboard.frame.particles.append(
                TextToast(bonus_position.get_position(), f"SPEED BONUS", font_size=10, color=(255, 100, 255)))
            bonus_position += Pose((0, 9))

    def on_fail_word(self):
        self.keyboard.frame.particles.append(
            TextToast((self.position + Pose((0, 15))).get_position(), f"INVALID WORD", font_size=10,
                      color=(255, 80, 80)))
        self.keyboard.frame.game.shake(2)

    def reset_word(self):
        self.current_string = ""
        self.on_current_string_update()
        self.since_time_start = 0
        self.timer_is_empty = False

