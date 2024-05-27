import math
import pygame


class Player:
    def __init__(self, x, y, size=50):
        self.rect = pygame.Rect(x, y, size, size)

        self.color = (0, 0, 0)
        self.angle = 0

        self.max_speed = 10
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = 0.6
        self.friction = 0.95

    def draw(self, screen):
        image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(image, self.color, (0, 0, self.rect.width, self.rect.height))

        new_image = pygame.transform.rotate(image, self.angle)
        new_rect = new_image.get_rect(center=self.rect.center)
        screen.blit(new_image, new_rect.topleft)

    def move(self, mouse, keys):
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

        dx, dy = (
            mouse[0] - self.rect.centerx,
            mouse[1] - self.rect.centery,
        )
        self.angle = (180 / math.pi) * -math.atan2(dy, dx)
