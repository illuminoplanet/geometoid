import math
import random
import pygame

from projectile import Projectile
from config import STAGE_PADDING, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT

########################### function 4 ##############################
pygame.mixer.init()
normal_laser_sound = pygame.mixer.Sound("assets/laser_sound1.mp3")
player_damage_sound = pygame.mixer.Sound("assets/player_damage_sound.mp3")
ultimate_sound = pygame.mixer.Sound("assets/ultimate_sound.mp3")
########################### function 4 ##############################


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
        self.max_health = self.health

        ##################### function 1 #########################
        self.last_ultimate_time = -25000  # 마지막 궁극기 사용 시간
        self.ultimate_cooldown = 20000  # 궁극기 쿨타임
        ##################### function 1 #########################

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

        ######################function2 ###############################
        # 체력 바 표시
        bar_width = 65
        bar_height = 15
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.image.get_height() // 2 - bar_height - 13

        # 현재 체력 비율 계산
        health_ratio = self.health / self.max_health

        # 배경 체력바
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))

        # 현재 체력 표시
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (bar_x, bar_y, bar_width * health_ratio, bar_height),
        )

        ######################function2 ###############################

        ######################function1 ###############################
        # 궁극기 쿨타임
        ult_bar_width = 65
        ult_bar_height = 15
        ult_bar_x = 1000
        ult_bar_y = 650

        # 현재 남은 궁극기 쿨타임 계산
        ultimate_time_left = (
            pygame.time.get_ticks() - self.last_ultimate_time
            if pygame.time.get_ticks() - self.last_ultimate_time < 20000
            else 20000
        )

        # 궁극기 쿨타임 배경바
        pygame.draw.rect(
            screen, (255, 0, 0), (ult_bar_x, ult_bar_y, ult_bar_width, ult_bar_height)
        )

        # 궁극기 쿨타임 표시
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (
                ult_bar_x,
                ult_bar_y,
                ult_bar_width * ultimate_time_left / 20000,
                ult_bar_height,
            ),
        )

        ######################function2 ###############################

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

        ######################## function 1 ##############################
        if (
            keys[pygame.K_r]
            and pygame.time.get_ticks() - self.last_ultimate_time >= 20000
        ):
            self.ultimate()
            self.last_ultimate_time = pygame.time.get_ticks()
        ######################## function 1 ##############################

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

            ########################### function 4 ##############################
            normal_laser_sound.play()
            ########################### function 4 ##############################

            self.prev_fire = current_time

        self.projectiles = [proj for proj in self.projectiles if not proj.destroyed]
        for proj in self.projectiles:
            proj.update()

    def take_damage(self, damage):
        self.health -= damage
        ####################### function 4 ###########################
        player_damage_sound.play()
        ####################### function 4 ###########################

    ########################### function 1 ##############################
    def ultimate(self):
        for i in range(200):
            center = self.rect.center + pygame.Vector2(
                math.cos(math.radians(self.angle)) * 32,
                -math.sin(math.radians(self.angle)) * 32,
            )
            proj = Projectile(self, center, random.randint(0, 359))
            self.projectiles.append(proj)
        ultimate_sound.play()
        ultimate_sound.play()


########################### function 1 ##############################
