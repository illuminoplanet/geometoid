import random
import pygame

from item import Health, Shot_Speed, Bomb
from enemy import Chaser, Shooter, Spreader
from config import *


class Stage:
    def __init__(self, padding):
        self.padding = padding

        self.round = 0
        self.pending_enemies = []
        self.enemies = []
        ############################
        ########## phase2 ##########
        ############################

        self.items = []

        ############################
        ########## phase2 ##########
        ############################

        self.rest = False

    def draw(self, screen, font):
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

        ############################
        ########## phase2 ##########
        ############################

        for item in self.items:
            item.draw(screen)

        ############################
        ########## phase2 ##########
        ############################

        if self.rest:
            text = font.render(f"Round {self.round}", True, BLACK)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))

    def update(self, player):
        for enemy in self.enemies:
            enemy.update(player.rect.center)
            if enemy.check_collision(player):
                player.take_damage(1)
                enemy.take_damage(100)
            for proj in player.projectiles:
                if enemy.check_collision(proj):
                    enemy.take_damage(1)
                    proj.destroyed = True
            for proj in enemy.projectiles:
                if player.rect.colliderect(proj.rect):
                    player.take_damage(1)
                    proj.destroyed = True

        ############################
        ########## phase2 ##########
        ############################
        for item in self.items:
            if item.check_collision(player):
                if isinstance(item, Health):
                    player.health = min(player.health + 5, 20)
                elif isinstance(item, Shot_Speed):
                    player.cooldown = max(player.cooldown-20, 100)
                elif isinstance(item, Bomb):
                    for enemy in self.enemies:
                        enemy.take_damage(10)
                item.used = True
        
        self.items = list(filter(lambda item: not item.used, self.items))
        # random item generation when enemy is killed
        tmp = list(filter(lambda enemy: enemy.health <= 0, self.enemies))
        if len(tmp) > 0:
            if random.random() < 0.4:
                enemy = random.choice(tmp)
                item_type = random.choice([Health, Shot_Speed, Bomb])
                self.items.append(item_type(enemy.x, enemy.y))
        ############################
        ########## phase2 ##########
        ############################
        
        self.enemies = list(filter(lambda enemy: enemy.health > 0, self.enemies))

        if len(self.enemies) == 0:
            if not self.rest:
                if len(self.pending_enemies) == 0:
                    self.round += 1
                    self.rest = True
                    pygame.time.set_timer(pygame.USEREVENT, 3000, True)
                else:
                    self.spawn_enemies()

    def plan_round(self):
        num_waves = self.round // 3 + 1
        for _ in range(num_waves):
            num_enemies = self.round // 2 + 1
            wave = []
            for _ in range(num_enemies):
                enemy_type = random.choice([Chaser, Shooter, Spreader])
                if random.random() < 0.5:
                    x = random.randint(64, SCREEN_WIDTH - 64)
                    y = random.choice([64, SCREEN_HEIGHT - 64])
                else:
                    x = random.choice([64, SCREEN_WIDTH - 64])
                    y = random.randint(64, SCREEN_HEIGHT - 64)

                wave.append(enemy_type(x, y))
            self.pending_enemies.append(wave)

        self.rest = False

    def spawn_enemies(self):
        self.enemies = self.pending_enemies.pop(0)
        for i, enemy in enumerate(self.enemies):
            enemy.create_time = pygame.time.get_ticks() + i * 300
