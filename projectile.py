import math
import pygame

from config import STAGE_PADDING, BLACK


class Projectile:
    def __init__(self, owner, pos, angle, speed=15):
        self.owner = owner
        self.image = pygame.transform.scale(owner.proj_image, (20, 16))
        self.rect = self.image.get_rect(center=pos)
        self.angle = angle
        self.speed = speed

        self.destroyed = False

    def update(self):
        self.velocity = pygame.math.Vector2(1, 0).rotate(-self.angle) * self.speed
        self.speed *= 1.02

        self.rect.center += self.velocity
        if (
            self.rect.left < STAGE_PADDING + 16
            or self.rect.right
            > pygame.display.get_surface().get_width() - STAGE_PADDING - 16
            or self.rect.top < STAGE_PADDING + 16
            or self.rect.bottom
            > pygame.display.get_surface().get_height() - STAGE_PADDING - 16
        ):
            self.destroyed = True

    def draw(self, screen):
        new_image = pygame.transform.rotate(
            self.image, self.velocity.angle_to(pygame.math.Vector2(1, 0))
        )
        new_rect = new_image.get_rect(center=self.rect.center)
        screen.blit(new_image, new_rect.topleft)
