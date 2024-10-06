import random

import pygame

from image_manager import ImageManager
from particle import Splat, TextToast
from primitives import Pose
import constants as c
from pyracy.sprite_tools import Sprite, Animation
from sound_manager import SoundManager


class Ant:

    def __init__(self, keyboard, path, speed = 1):
        self.hp = 1
        self.speed = speed
        self.keyboard = keyboard
        self.index_along_path = -1 if self.speed == 1 else random.randrange(-self.speed, 0)

        self.path = path
        self.position = keyboard.calculate_path_termination_position(path)
        self.direction = self.keyboard.calculate_direction_from_path(self.path)

        self.reached_destination = False
        self.dead = False
        self.target_position = self.position.copy()

        self.load_sprite()

        self.base_score = 100
        self.makes_allies_invulnerable = False

        self.protection = ImageManager.load("assets/images/protection.png")
        self.alert = ImageManager.load("assets/images/alert.png")

        self.squish_sfx = [SoundManager.load(f"assets/audio/squish_{i}.ogg") for i in range(1, 5)]

    def on_ant_turn(self):
        pass

    def load_sprite(self):
        self.left_face = Animation(
            ImageManager.load_copy("assets/images/ant_left.png"),
            (3, 1),
            3,
        )
        self.right_face = Animation(
            ImageManager.load_copy("assets/images/ant_left.png"),
            (3, 1),
            3,
            reverse_x=True,
        )
        self.down_left = Animation(
            ImageManager.load_copy("assets/images/ant_dl.png"),
            (3, 1),
            3,
        )
        self.down_right = Animation(
            ImageManager.load_copy("assets/images/ant_dl.png"),
            (3, 1),
            3,
            reverse_x=True
        )
        self.up_left = Animation(
            ImageManager.load_copy("assets/images/ant_ul.png"),
            (3, 1),
            3,
        )
        self.up_right = Animation(
            ImageManager.load_copy("assets/images/ant_ul.png"),
            (3, 1),
            3,
            reverse_x=True,
        )
        self.sprite = Sprite(6, (0, 0))

        if self.direction == c.UP_LEFT:
            self.sprite.add_animation({
                "Idle": self.up_left,
            }, loop=True)
        elif self.direction == c.DOWN_LEFT:
            self.sprite.add_animation({
                "Idle": self.down_left,
            }, loop=True)
        elif self.direction == c.LEFT:
            self.sprite.add_animation({
                "Idle": self.left_face,
            }, loop=True)
        elif self.direction == c.UP_RIGHT:
            self.sprite.add_animation({
                "Idle": self.up_right,
            }, loop=True)
        elif self.direction == c.DOWN_RIGHT:
            self.sprite.add_animation({
                "Idle": self.down_right,
            }, loop=True)
        elif self.direction == c.RIGHT:
            self.sprite.add_animation({
                "Idle": self.right_face,
            }, loop=True)
        self.sprite.start_animation("Idle")


    def get_current_letter(self):
        return self.path[self.index_along_path] if 0 <= self.index_along_path < len(self.path) else ""

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.advance()
        diff = self.target_position - self.position
        if diff.magnitude() > 3:
            max_speed = 30
            if diff.magnitude() > max_speed:
                diff.scale_to(max_speed)
            self.position += diff * dt * 8
        self.sprite.update(dt, events)

    def draw(self, surface, offset=(0, 0)):
        x = self.position.x + offset[0]
        y = self.position.y + offset[1]
        color = (50, 0, 0) if not self.dead else (100, 80, 80)

        if self.is_invulnerable() and not self.dead:
            surface.blit(self.protection, (x - self.protection.get_width()//2, y - self.protection.get_height()//2))

        surf_to_blit = self.sprite.get_image()
        if not self.dead:
            surface.blit(surf_to_blit, (x - surf_to_blit.get_width()//2, y - surf_to_blit.get_height()//2))
            if (len(self.path) - 1 < self.index_along_path + self.speed and not self.reached_destination):
                surface.blit(self.alert, (x - self.alert.get_width()//2, y - self.alert.get_height()//2))

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
        # self.position = self.keyboard.letter_to_key[letter].position.copy()

        self.keyboard.letter_to_key[letter].add(self)

    def reach_destination(self):
        self.target_position = self.keyboard.calculate_path_termination_position(self.path, False)
        if not self.reached_destination:
            self.keyboard.frame.particles.append(
                TextToast(self.position.get_position(), f"ESCAPED", font_size=10, color=(150, 150, 150)))
            self.reached_destination = True
            amt = self.keyboard.frame.lose_score(self.base_score)
            self.keyboard.frame.particles.append(
                TextToast((self.position + Pose((0, 16))).get_position(), f"-{amt}", font_size=10, color=(255, 100, 100)))

    def get_squashed(self):
        if self.is_invulnerable():
            self.invulnerable_hit()
            return
        self.hp -= 1
        if self.hp <= 0:
            self.die()

    def invulnerable_hit(self):
        bonus_position = self.position
        self.keyboard.frame.particles.append(
            TextToast(bonus_position.get_position(), f"INVULNERABLE", font_size=10, color=(77, 174, 226)))

    def die(self):
        if not self.dead:
            self.dead = True
            self.keyboard.frame.particles.append(Splat(self.position.get_position()))
            random.choice(self.squish_sfx).play()
            self.keyboard.frame.ants_killed_this_turn += 1
        score = self.keyboard.frame.gain_score(self.base_score)
        if (self.keyboard.frame.ants_killed_this_turn >= 3) and self.keyboard.frame.spree_level > 0:
            if self.keyboard.frame.spree_level == 1:
                score += 30 * (self.keyboard.frame.ants_killed_this_turn - 2)
            if self.keyboard.frame.spree_level == 2:
                score += 60 * (self.keyboard.frame.ants_killed_this_turn - 2)
        if (self.get_current_letter() and self.get_current_letter() in c.RARE_LETTERS):
            score *= self.keyboard.frame.rare_letter_modifier
        self.keyboard.frame.particles.append(TextToast(self.position.get_position(), f"+{score}", (255, 255, 0)))
        bonus_position = self.position + Pose((0, 18))
        if (self.get_current_letter() and self.get_current_letter() in c.RARE_LETTERS):
            self.keyboard.frame.particles.append(
                TextToast(bonus_position.get_position(), f"RARE LETTER", font_size=10, color=(255, 100, 255)))
            bonus_position += Pose((0, 9))
        if (self.keyboard.frame.ants_killed_this_turn >= 3) and self.keyboard.frame.spree_level > 0:
            self.keyboard.frame.particles.append(
                TextToast(bonus_position.get_position(), f"SPREE {self.keyboard.frame.ants_killed_this_turn}", font_size=10, color=(255, 180, 50)))
            bonus_position += Pose((0, 9))

    def set_target_position(self, pose):
        self.target_position = pose.copy()

    def is_invulnerable(self):
        letter = self.get_current_letter()
        if not letter:
            return False

        # Find my row/column
        column = -1
        row = -1
        for i, row_contents in enumerate(c.QWERTY_LAYOUT):
            if letter in row_contents:
                row = i
                column = row_contents.index(letter)

        neighboring_letters = [letter]

        # LR neighbors
        if column > 0:
            neighboring_letters += [c.QWERTY_LAYOUT[row][column - 1]]
        if column < len(c.QWERTY_LAYOUT[row]) - 1:
            neighboring_letters += [c.QWERTY_LAYOUT[row][column + 1]]

        # UDL neighbors
        if row > 0:
            neighboring_letters += [c.QWERTY_LAYOUT[row - 1][column]]
        if row < 2 and letter not in "LKP":
            neighboring_letters += [c.QWERTY_LAYOUT[row + 1][column]]

        # UDR neighbors
        if row > 0:
            neighboring_letters += [c.QWERTY_LAYOUT[row - 1][column + 1]]
        if row < 2 and letter not in "QAL":
            neighboring_letters += [c.QWERTY_LAYOUT[row + 1][column - 1]]

        for other_letter in neighboring_letters:
            for ant in self.keyboard.letter_to_key[other_letter].container:
                if ant.makes_allies_invulnerable and not ant.dead:
                    return True

        return False


class Persistant(Ant):
    def __init__(self, keyboard, path, speed = 1):
        super().__init__(keyboard, path, speed=speed)
        self.base_score = 300
        self.since_glitch = 0
        self.glitch_offset = Pose((0, 0))
        self.hp = 2

    def update(self, dt, events):
        super().update(dt, events)
        self.since_glitch += dt*1.5

        if self.since_glitch > 0.1:
            self.since_glitch = random.random() * -0.1
            self.glitch_offset = Pose((random.random() * 10 - 5, random.random() * 10 - 5))

    def draw(self, surface, offset=(0, 0)):
        if (self.since_glitch > 0 and self.since_glitch < 0.1) and self.hp > 1:
            offset = (Pose(offset) + self.glitch_offset * 0.1).get_position()
        super().draw(surface, offset)
        if (self.since_glitch > 0 and self.since_glitch < 0.1) and self.hp > 1:
            glitch_surf = self.sprite.get_image().copy()
            pose = self.position + Pose(offset) + self.glitch_offset
            x = pose.x - glitch_surf.get_width()//2
            y = pose.y - glitch_surf.get_height()//2
            glitch_surf.set_alpha(100)
            if not self.dead and not self.reached_destination:
                surface.blit(glitch_surf, (x, y))


    def get_squashed(self):
        super().get_squashed()
        if not self.is_invulnerable() and self.hp > 0:
            self.keyboard.frame.particles.append(
                TextToast(self.position.get_position(), f"SHIELDS DOWN", font_size=10, color=(255, 80, 50)))

    def on_ant_turn(self):
        if self.hp < 2 and not self.dead and not self.reached_destination:
            self.hp = 2
            self.keyboard.frame.particles.append(
                TextToast(self.position.get_position(), f"SHIELDS UP", font_size=10, color=(255, 80, 50)))

    def load_sprite(self):
        self.left_face = Animation(
            ImageManager.load_copy("assets/images/ant_left_extra_hit.png"),
            (3, 1),
            3,
        )
        self.right_face = Animation(
            ImageManager.load_copy("assets/images/ant_left_extra_hit.png"),
            (3, 1),
            3,
            reverse_x=True,
        )
        self.down_left = Animation(
            ImageManager.load_copy("assets/images/ant_dl_extra_hit.png"),
            (3, 1),
            3,
        )
        self.down_right = Animation(
            ImageManager.load_copy("assets/images/ant_dl_extra_hit.png"),
            (3, 1),
            3,
            reverse_x=True
        )
        self.up_left = Animation(
            ImageManager.load_copy("assets/images/ant_ul_extra_hit.png"),
            (3, 1),
            3,
        )
        self.up_right = Animation(
            ImageManager.load_copy("assets/images/ant_ul_extra_hit.png"),
            (3, 1),
            3,
            reverse_x=True,
        )
        self.sprite = Sprite(6, (0, 0))



        if self.direction == c.UP_LEFT:
            self.sprite.add_animation({
                "Idle": self.up_left,
            }, loop=True)
        elif self.direction == c.DOWN_LEFT:
            self.sprite.add_animation({
                "Idle": self.down_left,
            }, loop=True)
        elif self.direction == c.LEFT:
            self.sprite.add_animation({
                "Idle": self.left_face,
            }, loop=True)
        elif self.direction == c.UP_RIGHT:
            self.sprite.add_animation({
                "Idle": self.up_right,
            }, loop=True)
        elif self.direction == c.DOWN_RIGHT:
            self.sprite.add_animation({
                "Idle": self.down_right,
            }, loop=True)
        elif self.direction == c.RIGHT:
            self.sprite.add_animation({
                "Idle": self.right_face,
            }, loop=True)
        self.sprite.start_animation("Idle")


class Defendant(Ant):

    def __init__(self, keyboard, path, speed = 1):
        super().__init__(keyboard, path, speed=speed)
        self.makes_allies_invulnerable = True
        self.base_score = 250

    def is_invulnerable(self):
        return False

    def load_sprite(self):
        self.left_face = Animation(
            ImageManager.load_copy("assets/images/ant_left_shield.png"),
            (3, 1),
            3,
        )
        self.right_face = Animation(
            ImageManager.load_copy("assets/images/ant_left_shield.png"),
            (3, 1),
            3,
            reverse_x=True,
        )
        self.down_left = Animation(
            ImageManager.load_copy("assets/images/ant_dl_shield.png"),
            (3, 1),
            3,
        )
        self.down_right = Animation(
            ImageManager.load_copy("assets/images/ant_dl_shield.png"),
            (3, 1),
            3,
            reverse_x=True
        )
        self.up_left = Animation(
            ImageManager.load_copy("assets/images/ant_ul_shield.png"),
            (3, 1),
            3,
        )
        self.up_right = Animation(
            ImageManager.load_copy("assets/images/ant_ul_shield.png"),
            (3, 1),
            3,
            reverse_x=True,
        )
        self.sprite = Sprite(6, (0, 0))



        if self.direction == c.UP_LEFT:
            self.sprite.add_animation({
                "Idle": self.up_left,
            }, loop=True)
        elif self.direction == c.DOWN_LEFT:
            self.sprite.add_animation({
                "Idle": self.down_left,
            }, loop=True)
        elif self.direction == c.LEFT:
            self.sprite.add_animation({
                "Idle": self.left_face,
            }, loop=True)
        elif self.direction == c.UP_RIGHT:
            self.sprite.add_animation({
                "Idle": self.up_right,
            }, loop=True)
        elif self.direction == c.DOWN_RIGHT:
            self.sprite.add_animation({
                "Idle": self.down_right,
            }, loop=True)
        elif self.direction == c.RIGHT:
            self.sprite.add_animation({
                "Idle": self.right_face,
            }, loop=True)
        self.sprite.start_animation("Idle")


class Mutant(Ant):

    def __init__(self, keyboard, path, speed = 1):
        super().__init__(keyboard, path, speed=speed)
        self.base_score = 150

    def load_sprite(self):
        self.left_face = Animation(
            ImageManager.load_copy("assets/images/ant_left_spawner.png"),
            (3, 1),
            3,
        )
        self.right_face = Animation(
            ImageManager.load_copy("assets/images/ant_left_spawner.png"),
            (3, 1),
            3,
            reverse_x=True,
        )
        self.down_left = Animation(
            ImageManager.load_copy("assets/images/ant_dl_spawner.png"),
            (3, 1),
            3,
        )
        self.down_right = Animation(
            ImageManager.load_copy("assets/images/ant_dl_spawner.png"),
            (3, 1),
            3,
            reverse_x=True
        )
        self.up_left = Animation(
            ImageManager.load_copy("assets/images/ant_ul_spawner.png"),
            (3, 1),
            3,
        )
        self.up_right = Animation(
            ImageManager.load_copy("assets/images/ant_ul_spawner.png"),
            (3, 1),
            3,
            reverse_x=True,
        )
        self.sprite = Sprite(6, (0, 0))



        if self.direction == c.UP_LEFT:
            self.sprite.add_animation({
                "Idle": self.up_left,
            }, loop=True)
        elif self.direction == c.DOWN_LEFT:
            self.sprite.add_animation({
                "Idle": self.down_left,
            }, loop=True)
        elif self.direction == c.LEFT:
            self.sprite.add_animation({
                "Idle": self.left_face,
            }, loop=True)
        elif self.direction == c.UP_RIGHT:
            self.sprite.add_animation({
                "Idle": self.up_right,
            }, loop=True)
        elif self.direction == c.DOWN_RIGHT:
            self.sprite.add_animation({
                "Idle": self.down_right,
            }, loop=True)
        elif self.direction == c.RIGHT:
            self.sprite.add_animation({
                "Idle": self.right_face,
            }, loop=True)
        self.sprite.start_animation("Idle")