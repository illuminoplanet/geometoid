from abc import ABC, abstractmethod
import math
import random

import pygame

from projectile import Projectile
from config import STAGE_PADDING, BLACK


class Enemy:
    def __init__(self, x, y, speed, health):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health

        self.rect = pygame.Rect(x, y, 20, 20)
        self.proj_image = pygame.image.load("assets/proj_player.png")

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def draw(self, screen):
        raise NotImplementedError

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.destroy()

    def destroy(self):
        print("Enemy destroyed")
        pass

    def check_collision(self, other_rect):
        return self.rect.colliderect(other_rect)


class Chaser(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, speed=3, health=5)
        self.image = pygame.transform.scale(
            pygame.image.load("assets/chaser.png"), (28, 28)
        )
        self.rect = self.image.get_rect(center=(x, y))

        self.max_speed = 7
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = 0.7
        self.friction = 0.95

        self.trail = []
        self.prev_trail = 0

    def update(self, player_pos):
        self.direction = pygame.Vector2(player_pos) - pygame.Vector2(self.x, self.y)
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        self.velocity = (
            self.velocity * self.friction + self.direction * self.acceleration
        )
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.x += self.velocity.x
        self.y += self.velocity.y

        if pygame.time.get_ticks() - self.prev_trail > 40:
            self.trail.append((self.x, self.y, self.direction))
            if len(self.trail) > 15:
                self.trail.pop(0)
            self.prev_trail = pygame.time.get_ticks()

    def draw(self, screen):
        new_image = pygame.transform.rotate(
            self.image,
            -math.degrees(math.atan2(self.direction.y, self.direction.x)),
        )
        new_rect = new_image.get_rect(center=(self.x, self.y))
        screen.blit(new_image, new_rect.topleft)

        for i, (x, y, direction) in enumerate(self.trail):
            new_image = pygame.transform.rotate(
                self.image,
                -math.degrees(math.atan2(direction.y, direction.x)),
            )
            new_image.set_alpha(i * (150 // len(self.trail)))
            new_rect = new_image.get_rect(center=(x, y))
            screen.blit(new_image, new_rect.topleft)


class Shooter(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, speed=2, health=5)
        self.color = BLACK
        self.radius = 15
        self.cooldown = 200
        self.prev_fire = 0
        self.projectiles = []

    def update(self, player_pos):
        direction_vector = pygame.Vector2(player_pos) - pygame.Vector2(self.x, self.y)
        distance = direction_vector.length()
        if direction_vector.length() > 0:
            direction_vector = direction_vector.normalize()
        self.rect.topleft = (self.x, self.y)

        self.x += direction_vector.x * self.speed
        self.y += direction_vector.y * self.speed

        if distance < 320:
            current_time = pygame.time.get_ticks()
            if current_time - self.prev_fire > self.cooldown:
                angle = -math.degrees(
                    math.atan2(direction_vector.y, direction_vector.x)
                ) + random.randint(-5, 5)
                proj = Projectile(self, (self.x, self.y), angle, speed=5)
                self.projectiles.append(proj)
                self.prev_fire = current_time
            self.speed = 0
        else:
            self.speed = 2

        self.projectiles = [proj for proj in self.projectiles if not proj.destroyed]
        for proj in self.projectiles:
            proj.update()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        for proj in self.projectiles:
            proj.draw(screen)


class Spreader(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, speed=1, health=5)
        self.color = BLACK
        self.radius = 15
        self.cooldown = 1000
        self.prev_fire = 0
        self.projectiles = []

        self.direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))

    def update(self, player_pos):
        self.x += self.direction.x * self.speed
        self.y += self.direction.y * self.speed
        if (
            self.x < STAGE_PADDING + self.radius
            or self.x
            > pygame.display.get_surface().get_width() - STAGE_PADDING - self.radius
        ):
            self.direction.x *= -1
        if (
            self.y < STAGE_PADDING + self.radius
            or self.y
            > pygame.display.get_surface().get_height() - STAGE_PADDING - self.radius
        ):
            self.direction.y *= -1

        current_time = pygame.time.get_ticks()
        if current_time - self.prev_fire > self.cooldown:
            for angle in range(0, 360, 45):
                proj = Projectile(self, (self.x, self.y), angle, speed=5)
                self.projectiles.append(proj)
            self.prev_fire = current_time

        self.projectiles = [proj for proj in self.projectiles if not proj.destroyed]
        for proj in self.projectiles:
            proj.update()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        for proj in self.projectiles:
            proj.draw(screen)
