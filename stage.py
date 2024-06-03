import random
import pygame

from enemy import Chaser, Shooter, Spreader
from config import *


class Stage:
    def __init__(self, padding):
        self.padding = padding

        self.round = 0
        self.pending_enemies = []
        self.enemies = []

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, self.padding))
        pygame.draw.rect(screen, BLACK, (0, 0, self.padding, SCREEN_HEIGHT))
        pygame.draw.rect(
            screen, BLACK, (0, SCREEN_HEIGHT - self.padding, SCREEN_WIDTH, self.padding)
        )
        pygame.draw.rect(
            screen, BLACK, (SCREEN_WIDTH - self.padding, 0, self.padding, SCREEN_HEIGHT)
        )

        for enemy in self.enemies:
            enemy.draw(screen)

    def update(self, player):
        for enemy in self.enemies:
            enemy.update(player.rect.center)
            if enemy.check_collision(player):
                player.take_damage(1)
            for proj in player.projectiles:
                if enemy.check_collision(proj):
                    print("Hit")
                    enemy.take_damage(1)
                    proj.destroyed = True
            for proj in enemy.projectiles:
                if player.rect.colliderect(proj.rect):
                    player.take_damage(1)
                    proj.destroyed = True

        self.enemies = list(filter(lambda enemy: enemy.health > 0, self.enemies))

        if len(self.enemies) == 0:
            if len(self.pending_enemies) == 0:
                self.round += 1
                self.plan_round()

                print(f"Round {self.round}")
            else:
                self.spawn_enemies()

                print(f"Enemies remaining: {len(self.pending_enemies)}")

    def plan_round(self):
        num_waves = self.round // 3 + 1
        for _ in range(num_waves):
            num_enemies = self.round // 2 + 1
            for _ in range(num_enemies):
                enemy_type = random.choice([Chaser, Shooter, Spreader])
                if random.random() < 0.5:
                    x = random.randint(64, SCREEN_WIDTH - 64)
                    y = random.choice([64, SCREEN_HEIGHT - 64])
                else:
                    x = random.choice([64, SCREEN_WIDTH - 64])
                    y = random.randint(64, SCREEN_HEIGHT - 64)

                self.pending_enemies.append(enemy_type(x, y))

    def spawn_enemies(self):
        self.enemies.append(self.pending_enemies.pop(0))
