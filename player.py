import math
import random
import pygame

from projectile import Projectile
from config import STAGE_PADDING, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT

############################
########## phase2 ##########
############################
DARKGRAY = (59, 59, 59)
SHELL = (175, 156, 96)

def draw_gauge_bar(screen, width, height, percentage, bullets, reload):
    if not reload:
        text = pygame.font.SysFont("Arial", 20).render(f"Bullets: {bullets}", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH - width - text.get_width() - 10, 3))
    else:
        text = pygame.font.SysFont("Arial", 20).render("Reloading...", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH - width - text.get_width() - 10, 3))
    pygame.draw.rect(screen, DARKGRAY, (SCREEN_WIDTH - width - 5, 5, width, height))
    filled_width = int(width * percentage)
    pygame.draw.rect(screen, SHELL, (SCREEN_WIDTH - width - 5, 5, filled_width, height))
############################
########## phase2 ##########
############################

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

        ############################
        ########## phase2 ##########
        ############################
        self.max_bullets = 15
        self.bullets = 15
        self.reload = False
        self.reload_time = 500
        self.reload_start = 0
        ############################
        ########## phase2 ##########
        ############################

        self.cooldown = 300
        self.prev_fire = 0
        self.fire = False
        self.projectiles = []

    def draw(self, screen, font):
        if self.health <= 0:
            return

        for proj in self.projectiles:
            proj.draw(screen)

        new_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = new_image.get_rect(center=self.rect.center)
        screen.blit(new_image, new_rect.topleft)

        text = font.render(f"Health: {self.health}", True, self.color)
        screen.blit(text, (STAGE_PADDING, STAGE_PADDING))
        
        draw_gauge_bar(screen, 200, 20, self.bullets / self.max_bullets, self.bullets, self.reload)

    def update(self, mouse, keys):
        if self.health <= 0:
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

        ############################
        ########## phase2 ##########
        ############################
        if self.reload:
            if current_time - self.reload_start > self.reload_time and self.bullets < self.max_bullets:
                self.bullets += 1
                self.reload_start = current_time
                if self.bullets == self.max_bullets:
                    self.reload = False
        else:
            if self.fire and current_time - self.prev_fire > self.cooldown and self.bullets > 0:
                center = self.rect.center + pygame.Vector2(
                    math.cos(math.radians(self.angle)) * 32,
                    -math.sin(math.radians(self.angle)) * 32,
                )
                proj = Projectile(self, center, self.angle + random.randint(-5, 5))
                self.projectiles.append(proj)
                self.prev_fire = current_time
                self.bullets -= 1
            if self.bullets == 0:
                self.reload = True
                self.reload_start = current_time
        ############################
        ########## phase2 ##########
        ############################

        self.projectiles = [proj for proj in self.projectiles if not proj.destroyed]
        for proj in self.projectiles:
            proj.update()

    def take_damage(self, damage):
        self.health -= damage
