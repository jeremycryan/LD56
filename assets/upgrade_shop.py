import math
import random

import pygame

from image_manager import ImageManager
from primitives import Pose
import constants as c


class UpgradeShop:

    def __init__(self, frame):
        self.frame = frame
        self.position = Pose((c.WINDOW_WIDTH//2, - c.WINDOW_HEIGHT//2))
        self.floppies = []
        self.highlight_index = 1
        self.highlighted = None
        self.active = False
        self.choose_an_upgrade = ImageManager.load("assets/images/choose_an_upgrade.png")


    def populate(self):
        upgrades = self.frame.upgrades_player_could_pick()
        random.shuffle(upgrades)
        self.floppies = [
            Floppy(upgrades.pop(0), (-200, -15)),
            Floppy(upgrades.pop(0), (0, -50)),
            Floppy(upgrades.pop(0), (200, -15)),
        ]
        self.highlight_index = 1
        self.floppies[self.highlight_index].highlighted = True
        self.active = True

    def update(self, dt, events):
        hiddenness = 1 - self.frame.upgrade_screen_showingness
        y_factor = (hiddenness**2 * 2 - hiddenness) * hiddenness
        self.position = Pose((c.WINDOW_WIDTH//2, c.WINDOW_HEIGHT//2)) + Pose((0, -c.WINDOW_HEIGHT)) * y_factor
        for floppy in self.floppies:
            floppy.update(dt, events)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.floppies[self.highlight_index].highlighted = False
                    self.highlight_index -= 1
                    self.highlight_index %= 3
                    self.floppies[self.highlight_index].highlighted = True
                if event.key == pygame.K_RIGHT:
                    self.floppies[self.highlight_index].highlighted = False
                    self.highlight_index += 1
                    self.highlight_index %= 3
                    self.floppies[self.highlight_index].highlighted = True
                if event.key == pygame.K_RETURN:
                    self.select()

    def select(self):
        if self.frame.upgrade_screen_showingness < 0.99:
            return
        if not self.active:
            return
        self.active = False

        upgrade = None
        for floppy in self.floppies:
            if floppy.highlighted:
                upgrade = floppy.upgrade
                floppy.highlighted = False

        self.frame.gain_upgrade(upgrade[0])
        self.frame.hide_upgrade_screen()


    def draw(self, surface, offset=(0, 0)):
        if (self.frame.upgrade_screen_showingness < 0.01):
            return

        x = offset[0] + self.position.x
        y = offset[1] + self.position.y
        # pygame.draw.rect(surface, (255, 0, 0), (x - c.WINDOW_WIDTH//2, y- c.WINDOW_HEIGHT//2, c.WINDOW_WIDTH, c.WINDOW_HEIGHT), 5)

        for floppy in self.floppies:
            floppy.draw(surface, (x, y))

        surface.blit(self.choose_an_upgrade, (x - self.choose_an_upgrade.get_width()//2, y + 60))


class Floppy:

    def __init__(self, upgrade, position):
        self.position = Pose(position)
        self.upgrade = upgrade

        self.font = pygame.font.Font("assets/fonts/arial.ttf", 14)
        self.font.set_bold(True)
        self.name_string = self.font.render(upgrade[0], False, (0, 0, 0), bgcolor=(255, 255, 255))
        self.font = pygame.font.Font("assets/fonts/arial.ttf", 14)
        self.font.align = pygame.FONT_CENTER
        self.font.set_bold(False)
        self.description = self.font.render(upgrade[1], False, (0, 0, 0), wraplength=114, bgcolor=(255, 255, 255))

        self.start_time = random.random() * 100

        self.surf = pygame.image.load("assets/images/floppy.png")
        x = self.surf.get_width()//2
        y = self.surf.get_height()//2
        self.surf.blit(self.name_string, (x - self.name_string.get_width()//2, y - self.name_string.get_height()//2 - 0), special_flags=pygame.BLEND_MULT)
        self.surf.blit(self.description, (x - self.description.get_width()//2, y + 12), special_flags=pygame.BLEND_MULT)
        self.highlighted = False
        self.highlight = ImageManager.load("assets/images/highlight.png")

    def update(self, dt, events):
        self.start_time += dt

    def draw(self, surface, offset=(0, 0)):
        x = self.position.x + offset[0] + math.cos(self.start_time * 2) * 3
        y = self.position.y + offset[1] + math.sin(self.start_time * 2.1) * 3
        if (self.highlighted):
            surface.blit(self.highlight, (x - self.highlight.get_width()//2, y - self.highlight.get_height()//2))
        surface.blit(self.surf, (x - self.surf.get_width()//2, y - self.surf.get_height()//2))