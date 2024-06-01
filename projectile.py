import math
import pygame

from config import BLACK


class Projectile:
    def __init__(self, pos, angle, speed=15):
        self.rect = pygame.Rect(pos[0], pos[1], 6, 6)
        self.color = BLACK
        self.velocity = pygame.math.Vector2(
            math.cos(math.radians(angle)) * speed,
            -math.sin(math.radians(angle)) * speed,
        )

    def update(self):
        self.rect.center += self.velocity

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
