from abc import ABC, abstractmethod
import math

import pygame

from config import BLACK


class Enemy:
    def __init__(self, x, y, speed, health):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health

        self.rect = pygame.Rect(x, y, 20, 20)
        self.direction = pygame.Vector2(0, 0)

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
        self.color = BLACK
        self.radius = 15

    def update(self, player_pos):
        direction_vector = pygame.Vector2(player_pos) - pygame.Vector2(self.x, self.y)
        if direction_vector.length() > 0:
            direction_vector = direction_vector.normalize()

        self.x += direction_vector.x * self.speed
        self.y += direction_vector.y * self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
