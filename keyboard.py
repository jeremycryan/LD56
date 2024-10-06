from image_manager import ImageManager
from particle import Poof
from primitives import Pose
import constants as c
import pygame
import random
import math

from sound_manager import SoundManager
from target import Target


class Keyboard:

    def __init__(self, frame, position = (0, 0)):
        self.frame = frame
        self.position = Pose(position)
        self.keys = []
        self.letter_to_key = {}
        x0 = 103
        y = 164
        x_spacing = 44
        y_spacing = 44
        for row in c.QWERTY_LAYOUT:
            x = x0
            for letter in row:
                key = Key(letter, (x, y), frame)
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

        self.outside_sprite = ImageManager.load("assets/images/outside_keyboard.png")
        self.inside_sprite = ImageManager.load("assets/images/inside_keyboard.png")

        self.key_punch_sfx = SoundManager.load("assets/audio/key_attack.ogg")
        self.key_punch_sfx.set_volume(0.3)

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
        surface.blit(self.inside_sprite, (xo, yo))
        surface.blit(self.outside_sprite, (xo, yo))
        for key in self.keys:
            key.draw(surface, offset=(xo, yo))

    def draw_late(self, surface, offset=(0, 0)):
        xo = offset[0] + self.position.x
        yo = offset[1] + self.position.y
        surface.blit(self.outside_sprite, (xo, yo))
        for key in self.keys:
            key.draw_late(surface, offset)

    def calculate_path_termination_position(self, path, start=True):
        a = path[0] if start else path[-1]
        b = path[1] if start else path[-2]
        diff = self.letter_to_key[a].position - self.letter_to_key[b].position
        return self.letter_to_key[a].position + diff

    def calculate_direction_from_path(self, path):
        if path in self.horizontal_paths:
            return c.RIGHT
        if path in self.vertical_paths_left:
            return c.UP_LEFT
        if path in self.vertical_paths_right:
            return c.UP_RIGHT
        path = path[::-1]
        if path in self.horizontal_paths:
            return c.LEFT
        if path in self.vertical_paths_left:
            return c.DOWN_RIGHT
        if path in self.vertical_paths_right:
            return c.DOWN_LEFT
        raise

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
            self.key_punch_sfx.play()
            self.letter_to_key[letter].squash()
            if letter in self.targets:
                target = self.targets[letter]
                if target.intensity == 1:
                    target.dismiss()
                else:
                    target.update_intensity(target.intensity - 1)


class Key:

    def __init__(self, letter, position, frame):
        self.letter = letter
        self.position = Pose(position)
        self.container = []
        self.font = pygame.sysfont.SysFont("monospace", 18, bold=True)
        self.letter_surface = self.font.render(self.letter, False, (128, 128, 128))
        self.count = 0
        self.backplate = ImageManager.load("assets/images/key_outline.png")
        self.fill = ImageManager.load_copy("assets/images/key_full.png")
        self.fill.blit(self.letter_surface, (self.fill.get_width()//2 - self.letter_surface.get_width()//2 - 10, self.fill.get_height()//2 - self.letter_surface.get_height()//2 - 10))
        self.fill.set_colorkey((255, 0, 0))
        self.frame = frame

        self.since_squish = 999
        self.bomb = ImageManager.load("assets/images/cherry_bomb.png")
        self.bomb.set_colorkey((255, 255, 255))

        self.explosive = False

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

        surface.blit(self.backplate, (x - self.backplate.get_width()//2, y - self.backplate.get_height()//2))
        surface.blit(self.letter_surface, (x - self.letter_surface.get_width()//2 - 10, y - self.letter_surface.get_height()//2 - 10))

        if (self.explosive):
            surface.blit(self.bomb, (x - self.bomb.get_width()//2, y - self.bomb.get_height()//2), special_flags=pygame.BLEND_MULT)



    def draw_late(self, surface, offset=(0, 0)):
        x = self.position.x + offset[0]
        y = self.position.y + offset[1]

        alpha = 255 - 512 * self.since_squish
        if alpha < 0:
            alpha = 0
        self.fill.set_alpha(alpha)

        if self.since_squish < 0.5:
            surface.blit(self.fill, (x - self.fill.get_width()//2, y - self.fill.get_height()//2))

    def update(self, dt, events):
        if self.count != len(self.container):
            self.count = len(self.container)
        self.assign_target_positions()

        self.since_squish += dt


    def squash(self, avoid_recursion = False):
        for ant in self.container[:]:
            ant.get_squashed()
            if ant.dead:
                self.container.remove(ant)
        for i in range(20):
            self.frame.particles.append(Poof(self.position.get_position()))

        if not avoid_recursion:
            self.frame.game.shake(5)

        self.since_squish = 0

        if not avoid_recursion and self.explosive:
            column = -1
            row = -1
            for i, row_contents in enumerate(c.QWERTY_LAYOUT):
                if self.letter in row_contents:
                    row = i
                    column = row_contents.index(self.letter)

            neighboring_letters = [self.letter]

            # LR neighbors
            if column > 0:
                neighboring_letters += [c.QWERTY_LAYOUT[row][column - 1]]
            if column < len(c.QWERTY_LAYOUT[row]) - 1:
                neighboring_letters += [c.QWERTY_LAYOUT[row][column + 1]]

            # UDL neighbors
            if row > 0:
                neighboring_letters += [c.QWERTY_LAYOUT[row - 1][column]]
            if row < 2 and self.letter not in "LKP":
                neighboring_letters += [c.QWERTY_LAYOUT[row + 1][column]]

            # UDR neighbors
            if row > 0:
                neighboring_letters += [c.QWERTY_LAYOUT[row - 1][column + 1]]
            if row < 2 and self.letter not in "QAL":
                neighboring_letters += [c.QWERTY_LAYOUT[row + 1][column - 1]]

            for other_letter in neighboring_letters:
                other_key = self.frame.keyboard.letter_to_key[other_letter]
                other_key.squash(True)

    def assign_target_positions(self):
        self.container.sort(key = (lambda x: 1 if x.is_invulnerable() else 0))
        if len(self.container) == 1:
            self.container[0].set_target_position(self.position)
            return
        if not self.container:
            return
        angle = -60
        spacing = 360/len(self.container)
        distance_from_center = 12
        for ant in self.container:
            rads = angle/180*math.pi
            x = math.cos(rads)*distance_from_center
            y = math.sin(rads)*distance_from_center
            ant.set_target_position(self.position + Pose((x, y)))
            angle -= spacing