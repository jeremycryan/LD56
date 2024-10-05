from image_manager import ImageManager
from primitives import Pose
import pygame


class Target:

    START_SCALE = 2
    START_ALPHA = 0

    def __init__(self, position = (0, 0)):
        self.sprite = ImageManager.load_copy("assets/images/crosshairs.png")
        self.target_scale = 1
        self.target_alpha = 255
        self.intensity = 1

        self.alpha = Target.START_ALPHA
        self.scale = Target.START_SCALE

        self.position = Pose(position)
        self.width = 50

        self.destroyed = False

    def update(self, dt, events):
        if (self.alpha < self.target_alpha):
            self.alpha += dt*1500
            if self.alpha > self.target_alpha:
                self.alpha = self.target_alpha

        if self.scale > self.target_scale:
            self.scale -= dt * 6
            if self.scale < self.target_scale:
                self.scale = self.target_scale

    def draw(self, surface, offset=(0, 0)):
        scaled = pygame.transform.scale(self.sprite, (int(self.width * self.scale), int(self.width * self.scale)))
        scaled.set_alpha(self.alpha)
        x = offset[0] + self.position.x - scaled.get_width()//2
        y = offset[1] + self.position.y - scaled.get_height()//2
        surface.blit(scaled, (x, y))

    def dismiss(self):
        self.alpha = 0
        self.destroyed = True

    def update_intensity(self, new_val):
        if new_val == self.intensity:
            return
        self.scale = max(self.scale, 1.2)
        self.intensity = new_val
