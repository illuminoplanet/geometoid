import math
import random
import pygame

from projectile import Projectile
from config import STAGE_PADDING, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT


class Player:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(
            pygame.image.load("assets/player.png"), (64, 64)
        )
        self.proj_image = pygame.image.load("assets/proj_player.png")

        self.rect = self.image.get_rect(center=(x, y))

        self.color = (0, 0, 0)
        self.angle = 0
        self.health = 20

        self.max_speed = 10
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = 0.6
        self.friction = 0.95

        self.cooldown = 100
        self.prev_fire = 0
        self.fire = False
        self.projectiles = []

        self.alive = False

    def draw(self, screen, font):
        if self.health <= 0:
            text = font.render("Game Over", True, self.color)
            screen.blit(
                text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2)
            )
            return

        for proj in self.projectiles:
            proj.draw(screen)

        new_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = new_image.get_rect(center=self.rect.center)
        screen.blit(new_image, new_rect.topleft)

        text = font.render(f"Health: {self.health}", True, self.color)
        screen.blit(text, (STAGE_PADDING, STAGE_PADDING))

    def update(self, mouse, keys):
        if self.health <= 0:
            self.alive = False
            return

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

        self.x = self.rect.centerx
        self.y = self.rect.centery

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
            center = self.rect.center + pygame.Vector2(
                math.cos(math.radians(self.angle)) * 32,
                -math.sin(math.radians(self.angle)) * 32,
            )
            proj = Projectile(self, center, self.angle + random.randint(-5, 5))
            self.projectiles.append(proj)
            self.prev_fire = current_time

        self.projectiles = [proj for proj in self.projectiles if not proj.destroyed]
        for proj in self.projectiles:
            proj.update()

    def take_damage(self, damage):
        self.health -= damage

    def damage_effect(surface, scale):
        GB = min(255, max(0, round(255 * (1-scale))))
        surface.fill((255, GB, GB), special_flags = pygame.BLEND_MULT)