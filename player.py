import math
import random
import pygame

from projectile import Projectile
from config import STAGE_PADDING


class Player:
    def __init__(self, x, y, size=50):
        self.rect = pygame.Rect(x, y, size, size)

        self.color = (0, 0, 0)
        self.angle = 0
        self.health = 100

        self.max_speed = 10
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = 0.6
        self.friction = 0.95

        self.cooldown = 100
        self.prev_fire = 0
        self.fire = False
        self.projectiles = []

    def draw(self, screen):
        image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(image, self.color, (0, 0, self.rect.width, self.rect.height))

        new_image = pygame.transform.rotate(image, self.angle)
        new_rect = new_image.get_rect(center=self.rect.center)
        screen.blit(new_image, new_rect.topleft)

        for proj in self.projectiles:
            proj.draw(screen)

    def update(self, mouse, keys):
        accel = pygame.math.Vector2(0, 0)
        if keys[pygame.K_a]:
            accel.x -= self.acceleration
        if keys[pygame.K_d]:
            accel.x += self.acceleration
        if keys[pygame.K_w]:
            accel.y -= self.acceleration
        if keys[pygame.K_s]:
            accel.y += self.acceleration

        self.velocity = (self.velocity + accel) * self.friction
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        self.rect.center += self.velocity

        self.rect.clamp_ip(
            pygame.Rect(
                STAGE_PADDING,
                STAGE_PADDING,
                pygame.display.get_surface().get_width() - STAGE_PADDING * 2,
                pygame.display.get_surface().get_height() - STAGE_PADDING * 2,
            )
        )

        dx, dy = (
            mouse[0] - self.rect.centerx,
            mouse[1] - self.rect.centery,
        )
        self.angle = (180 / math.pi) * -math.atan2(dy, dx)

        current_time = pygame.time.get_ticks()
        if self.fire and current_time - self.prev_fire > self.cooldown:
            proj = Projectile(
                self, self.rect.center, self.angle + random.randint(-5, 5)
            )
            self.projectiles.append(proj)
            self.prev_fire = current_time

        self.projectiles = [proj for proj in self.projectiles if not proj.destroyed]
        for proj in self.projectiles:
            proj.update()

    def take_damage(self, damage):
        self.health -= damage
