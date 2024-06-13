import random
import pygame

from enemy import Chaser, Shooter, Spreader, Boss
from config import *


class Stage:
    def __init__(self, padding):
        self.padding = padding

        self.round = 0
        self.pending_enemies = []
        self.enemies = []

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
                    if enemy.health <= 0:
                        ########## PHASE2 ##########
                        player.fuel = min(player.fuel + 20, player.max_fuel)  # 연료 충전
                        player.score += 1
            for proj in enemy.projectiles:
                if player.rect.colliderect(proj.rect):
                    player.take_damage(1)
                    proj.destroyed = True

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
            ############################
            ########## PHASE2 ##########
            ############################
            if self.round % 5 == 0:  # 5라운드마다 보스 등장
                wave = [Boss(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
            else:
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
            ############################
            ########## PHASE2 ##########
            ############################
            self.pending_enemies.append(wave)

        self.rest = False

    def spawn_enemies(self):
        self.enemies = self.pending_enemies.pop(0)
        for i, enemy in enumerate(self.enemies):
            enemy.create_time = pygame.time.get_ticks() + i * 300
