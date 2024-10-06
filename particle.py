import math
import random

import pygame

from image_manager import ImageManager
from primitives import Pose


class Particle:

    def __init__(self, position=(0, 0), velocity=(0, 0), duration=1.0):
        self.position = Pose(position)
        self.velocity = Pose(velocity)
        self.destroyed = False
        self.duration = duration
        self.age = 0
        self.layer = 1

    def get_scale(self):
        return 1

    def update(self, dt, events):
        if self.destroyed:
            return
        self.position += self.velocity * dt
        if self.age > self.duration:
            self.destroy()
        self.age += dt

    def draw(self, surf, offset=(0, 0)):
        if self.destroyed:
            return

    def through(self):
        return min(0.999, self.age/self.duration)

    def destroy(self):
        self.destroyed = True


class Poof(Particle):

    def __init__(self, position):
        self.surface = ImageManager.load_copy("assets/images/poof.png")
        angle = random.random() * 2 * math.pi
        vx = math.cos(angle)
        vy = math.sin(angle)
        velocity = (vx * random.random() * 200, vy*random.random()*200)
        super().__init__(position, velocity, random.random() * 0.5 + 0.5)
        self.position += Pose((vx*15, vy*15))
        self.angle = random.random() * 360

    def get_scale(self):
        return 1 - self.through()

    def update(self, dt, events):
        self.velocity *= 0.06**dt
        self.surface.set_alpha(100 * (1 - self.through()))
        super().update(dt, events)
        self.angle += 60*dt

    def draw(self, surf, offset=(0, 0)):
        to_draw = pygame.transform.scale(self.surface, (int(self.surface.get_width() * self.get_scale()), int(self.surface.get_height() * self.get_scale())))
        to_draw = pygame.transform.rotate(to_draw, self.angle)
        x = self.position.x + offset[0]
        y = self.position.y + offset[1]
        surf.blit(to_draw, (x - to_draw.get_width()//2, y - to_draw.get_height()//2))


class Splat(Particle):

    def __init__(self, position):
        self.sprite = ImageManager.load(f"assets/images/splat_{random.randrange(0, 5)}.png")
        angle = random.choice((0, 90, 180, 270))
        self.sprite = pygame.transform.rotate(self.sprite, angle)
        self.sprite.set_alpha(100)
        super().__init__(position, (0, 0), 9999999999)

    def draw(self, surf, offset=(0, 0)):
        x = self.position.x + offset[0]
        y = self.position.y + offset[1]
        surf.blit(self.sprite, (x - self.sprite.get_width()//2, y - self.sprite.get_height()//2))


class TextToast(Particle):

    FONTS = {}

    def __init__(self, position, text, color = (255, 255, 255), font_size = 20):
        super().__init__(position, (0, -50), 0.8)

        if font_size not in TextToast.FONTS:
            TextToast.FONTS[font_size] = pygame.font.Font("assets/fonts/a_goblin_appears.ttf", font_size)

        self.surface = pygame.Surface((150, 50))
        self.surface.fill((255, 0, 0))
        self.surface.set_colorkey((255, 0, 0))
        black_text = TextToast.FONTS[font_size].render(text, 0, (0, 0, 0))
        for offset in [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 3)]:
            x = self.surface.get_width()//2 - black_text.get_width()//2
            y = self.surface.get_height()//2 - black_text.get_height()//2
            self.surface.blit(black_text, (x + offset[0], y + offset[1]))
        self.surface.blit(TextToast.FONTS[font_size].render(text, 0, (color)), (self.surface.get_width()//2 - black_text.get_width()//2, self.surface.get_height()//2 - black_text.get_height()//2))
        self.layer = 2


    def get_scale(self):
        return 0.7 + 0.3*self.through()

    def get_alpha(self):
        return 255 - 255 * self.through()**2

    def update(self, dt, events):
        super().update(dt, events)
        self.velocity *= 0.1**dt

    def draw(self, surface, offset=(0, 0)):

        my_surf = self.surface  #my_surf = pygame.transform.scale(self.surface, (int(self.surface.get_width() * self.get_scale()), int(self.surface.get_height() * self.get_scale())))
        my_surf.set_alpha(self.get_alpha())
        x = offset[0] + self.position.x
        y = offset[1] + self.position.y
        surface.blit(my_surf, (x - my_surf.get_width()//2, y - my_surf.get_height()//2))