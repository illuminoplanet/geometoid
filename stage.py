import random
import pygame

from enemy import Chaser, Shooter, Spreader
from config import *
from player import Player

class Stage:
    def __init__(self, padding, screen, player):
        self.padding = padding
########################## PHASE 2 #########################
        self.screen = screen
        self.player = player
############################################################

        self.round = 0
        self.pending_enemies = []
        self.enemies = []

        self.rest = False
########################## PHASE 2 #########################
        self.damage_effect_timer = 0
        self.damage = 1
        self.invincible_timer = 0
        self.player_image = self.player.image
        self.playercolor = 0
        self.ATK = 100
        self.isInvincible = False

    def invincible(self):
        if self.invincible_timer <= 0: 
            self.damage = 1
            self.player.image = self.player.image_original.copy()
            self.ATK = 100
            self.isInvincible = False

        else:
            self.damage = 0
            self.ATK = 1000
            
            color = pygame.Color(0)
            color.hsla = (self.playercolor, 100, 50, 100)
            self.playercolor = self.playercolor + 2 if self.playercolor < 360 else 0 

            rainbow_player = pygame.Surface(self.player_image.get_size()).convert_alpha()
            rainbow_player.fill(color)
            self.player.image = self.player.image_original.copy()
            self.player.image.blit(rainbow_player, (0,0), special_flags = pygame.BLEND_RGBA_MULT)
            
            
            self.invincible_timer -= 1
            self.isInvincible = True

############################################################

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
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50) )

########################## PHASE 2 #########################
    def damage_effect(self, scale):
        if(self.damage_effect_timer > 0):
            GB = min(255, max(0, round(255 * (1-scale))))
            self.screen.fill((255, GB, GB), special_flags = pygame.BLEND_MULT)
            self.damage_effect_timer -= 1
############################################################

    def update(self, player):
        self.invincible()
        if not self.isInvincible:
            self.damage_effect(0.5)

        for enemy in self.enemies:
            enemy.update(player.rect.center)
            if enemy.check_collision(player):
                player.take_damage(self.damage)
########################## PHASE 2 #########################
                if not self.isInvincible: self.damage_effect_timer = 10
############################################################
                enemy.take_damage(self.ATK)
            for proj in player.projectiles:
                if enemy.check_collision(proj):
                    enemy.take_damage(1)
                    proj.destroyed = True
            for proj in enemy.projectiles:
                if player.rect.colliderect(proj.rect):
                    player.take_damage(self.damage)
########################## PHASE 2 #########################
                    if not self.isInvincible: self.damage_effect_timer = 10
############################################################
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

########################## PHASE 2 #########################

############################################################

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
