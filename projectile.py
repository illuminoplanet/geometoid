import math
import pygame

from config import STAGE_PADDING, BLACK


class Projectile:
    def __init__(self, owner, pos, angle, speed=15):
        self.owner = owner
        self.rect = pygame.Rect(pos[0], pos[1], 6, 6)
        self.color = BLACK
        self.velocity = pygame.math.Vector2(
            math.cos(math.radians(angle)) * speed,
            -math.sin(math.radians(angle)) * speed,
        )

        self.destroyed = False

    def update(self):
        self.rect.center += self.velocity
        if self.rect.colliderect(
            pygame.Rect(0, 0, pygame.display.get_surface().get_width(), STAGE_PADDING)
        ):
            self.destroyed = True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
