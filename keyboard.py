from primitives import Pose
import constants as c
import pygame
import random

from target import Target


class Keyboard:

    def __init__(self, frame, position = (0, 0)):
        self.frame = frame
        self.position = Pose(position)
        self.keys = []
        self.letter_to_key = {}
        x0 = 50
        y = 150
        x_spacing = 50
        y_spacing = 50
        for row in c.QWERTY_LAYOUT:
            x = x0
            for letter in row:
                key = Key(letter, (x, y))
                self.keys.append(key)
                self.letter_to_key[letter] = key
                x += x_spacing
            y += y_spacing
            x0 += x_spacing//2

        self.horizontal_paths = []
        for row in c.QWERTY_LAYOUT:
            self.horizontal_paths.append(row)

        self.vertical_paths_left = []
        self.vertical_paths_right = []
        for i, letter in enumerate(c.QWERTY_LAYOUT[2]):
            l_path = letter + c.QWERTY_LAYOUT[1][i] + c.QWERTY_LAYOUT[0][i]
            r_path = letter + c.QWERTY_LAYOUT[1][i+1] + c.QWERTY_LAYOUT[0][i+2]
            self.vertical_paths_left.append(l_path)
            self.vertical_paths_right.append(r_path)

        self.all_paths = []
        for path in self.horizontal_paths + self.vertical_paths_left + self.vertical_paths_right:
            self.all_paths.append(path)
            self.all_paths.append(path[::-1])

        self.target_string = ""
        self.targets = {}

    def random_horizontal_path(self):
        path = random.choice(self.horizontal_paths)
        if (random.random() < 0.5):
            path = path[::-1]
        return path

    def random_vertical_path(self):
        path = random.choice(self.vertical_paths_right + self.vertical_paths_left)
        if (random.random() < 0.5):
            path = path[::-1]
        return path

    def update(self, dt, events):
        for key in self.keys:
            key.update(dt, events)

    def draw(self, surface, offset=(0, 0)):
        xo = offset[0] + self.position.x
        yo = offset[1] + self.position.y
        for key in self.keys:
            key.draw(surface, offset=(xo, yo))

    def calculate_path_termination_position(self, path, start=True):
        a = path[0] if start else path[-1]
        b = path[1] if start else path[-2]
        diff = self.letter_to_key[a].position - self.letter_to_key[b].position
        return self.letter_to_key[a].position + diff

    def update_targets(self, new_string):
        old_string = self.target_string
        self.target_string = new_string
        for letter in new_string:
            if letter not in old_string:
                new_target = Target(self.letter_to_key[letter].position.copy().get_position())
                self.targets[letter] = new_target
                self.frame.targets.append(new_target)
            elif new_string.count(letter) != old_string.count(letter):
                self.targets[letter].update_intensity(new_string.count(letter))
        for letter in old_string:
            if letter not in new_string:
                if letter in self.targets:
                    self.targets.pop(letter).dismiss()

    def process_word(self, current_string):
        for letter in current_string:
            self.letter_to_key[letter].squash()
            if letter in self.targets:
                target = self.targets[letter]
                if target.intensity == 1:
                    target.dismiss()
                else:
                    target.update_intensity(target.intensity - 1)


class Key:

    def __init__(self, letter, position):
        self.letter = letter
        self.position = Pose(position)
        self.container = []
        self.font = pygame.sysfont.SysFont("monospace", 20)
        self.letter_surface = self.font.render(self.letter, True, (0, 255, 0))

    def add(self, ant):
        if ant:
            self.container.append(ant)

    def remove(self, ant):
        if ant in self.container:
            self.container.remove(ant)
            return ant
        return None

    def draw(self, surface, offset=(0, 0)):
        x = self.position.x + offset[0]
        y = self.position.y + offset[1]

        pygame.draw.rect(surface, (100, 100, 100), (x - 20, y - 20, 40, 40))
        surface.blit(self.letter_surface, (x - self.letter_surface.get_width()//2 - 10, y - self.letter_surface.get_height()//2 - 10))

    def update(self, dt, events):
        pass

    def squash(self):
        for ant in self.container[:]:
            ant.get_squashed()
            if ant.dead:
                self.container.remove(ant)