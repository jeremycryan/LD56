import random

import pygame
from primitives import Pose



class Ant:

    def __init__(self, keyboard, path):
        self.hp = 1
        self.speed = 2
        self.keyboard = keyboard
        self.index_along_path = -1 if self.speed == 1 else random.randrange(-self.speed, -1)

        self.path = path
        self.position = keyboard.calculate_path_termination_position(path)

        self.reached_destination = False
        self.dead = False

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.advance()

    def draw(self, surface, offset=(0, 0)):
        x = self.position.x + offset[0]
        y = self.position.y + offset[1]
        color = (255, 255, 0) if not self.dead else (50, 50, 0)
        pygame.draw.circle(surface, color, (x, y), 6)

    def advance(self):
        if self.dead:
            return

        old_letter = self.path[self.index_along_path] if self.index_along_path < len(self.path) and self.index_along_path >= 0 else ""
        if old_letter:
            self.keyboard.letter_to_key[old_letter].remove(self)

        self.index_along_path += self.speed
        if len(self.path) <= self.index_along_path:
            self.reach_destination()
            return
        letter = self.path[self.index_along_path]
        self.position = self.keyboard.letter_to_key[letter].position.copy()

        self.keyboard.letter_to_key[letter].add(self)

    def reach_destination(self):
        self.position = self.keyboard.calculate_path_termination_position(self.path, False)
        if not self.reached_destination:
            print("OUCH")
            self.reached_destination = True

    def get_squashed(self):
        self.hp -= 1
        if self.hp <= 0:
            self.die()

    def die(self):
        if not self.dead:
            self.dead = True