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
        self.score = 0

        self.max_fuel = 100
        self.fuel = 100
        self.fuel_depletion_rate = 5  # 연료 소모
        self.fuel_recharge_rate = 2  # 연료 재충전

    def draw(self, screen, font):
        if self.health <= 0:
            game_over_text = font.render("Game Over", True, self.color)
            score_text = font.render(f"Score = {self.score}", True, self.color)
            screen.blit(
                game_over_text, 
                (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20)
            )
            screen.blit(
                score_text, 
                (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 20)
            )
            return

        for proj in self.projectiles:
            proj.draw(screen)

        new_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = new_image.get_rect(center=self.rect.center)
        screen.blit(new_image, new_rect.topleft)

        text1 = font.render(f"Health: {self.health}", True, self.color)
        text2 = font.render(f"Score: {self.score}", True, self.color)
        screen.blit(text1, (STAGE_PADDING, STAGE_PADDING))
        screen.blit(text2, (STAGE_PADDING, STAGE_PADDING + 30))

        # 연료 게이지 표시
        fuel_ratio = self.fuel / self.max_fuel
        fuel_bar_width = 200
        fuel_bar_height = 20
        fuel_bar_x = STAGE_PADDING
        fuel_bar_y = SCREEN_HEIGHT - STAGE_PADDING - fuel_bar_height - 10
        pygame.draw.rect(screen, (0, 0, 0), (fuel_bar_x, fuel_bar_y, fuel_bar_width, fuel_bar_height), 2)  # 검정색 테두리
        pygame.draw.rect(screen, (0, 255, 0), (fuel_bar_x, fuel_bar_y, fuel_bar_width * fuel_ratio, fuel_bar_height))  # 초록색 연료 게이지


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
        if self.fire and current_time - self.prev_fire > self.cooldown:
            center = self.rect.center + pygame.Vector2(
                math.cos(math.radians(self.angle)) * 32,
                -math.sin(math.radians(self.angle)) * 32,
            )
            proj = Projectile(self, center, self.angle + random.randint(-5, 5))
            self.projectiles.append(proj)      

            # 스페이스 바를 누르고 있을 때 추가 총알 발사
            if keys[pygame.K_SPACE] and self.fuel > 0:
                angles = [-6, 6]  # 3갈래 발사 각도
                for angle_offset in angles:
                    extra_proj = Projectile(self, center, self.angle + angle_offset)
                    self.projectiles.append(extra_proj)
                self.fuel -= self.fuel_depletion_rate  # 연료 소모

            self.prev_fire = current_time

        self.projectiles = [proj for proj in self.projectiles if not proj.destroyed]
        for proj in self.projectiles:
            proj.update()

    def take_damage(self, damage):
        self.health -= damage
