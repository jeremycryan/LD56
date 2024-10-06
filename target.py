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
        self.width = 80

        self.destroyed = False
        self.dismissing = False

    def update(self, dt, events):
        if (self.alpha < self.target_alpha) and not self.dismissing:
            self.alpha += dt*1500
            if self.alpha > self.target_alpha:
                self.alpha = self.target_alpha

        if self.scale > self.target_scale and not self.dismissing:
            self.scale -= dt * 6
            if self.scale < self.target_scale:
                self.scale = self.target_scale

        if self.dismissing:
            self.scale -= dt * 2
            self.alpha -= 2500 * dt
            if self.alpha < 0 or self.scale < 0:
                self.destroyed = True

    def draw(self, surface, offset=(0, 0)):
        scaled = pygame.transform.scale(self.sprite, (int(self.width * self.scale), int(self.width * self.scale)))
        scaled.set_alpha(self.alpha)
        x = offset[0] + self.position.x - scaled.get_width()//2
        y = offset[1] + self.position.y - scaled.get_height()//2
        surface.blit(scaled, (x, y))

    def dismiss(self):
        self.dismissing = True

    def update_intensity(self, new_val):
        if new_val == self.intensity:
            return
        self.scale = max(self.scale, 1.3)
        self.intensity = new_val
