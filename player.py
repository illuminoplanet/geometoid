import math
import pygame


class Player:
    def __init__(self, x, y, size=50):
        self.rect = pygame.Rect(x, y, size, size)

        self.color = (0, 0, 0)
        self.speed = 5

    def draw(self, screen):
        image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(image, self.color, (0, 0, self.rect.width, self.rect.height))

        new_image = pygame.transform.rotate(image, self.angle)
        new_rect = new_image.get_rect(center=self.rect.center)
        screen.blit(new_image, new_rect.topleft)

    def move(self, mouse, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

        dx, dy = (
            mouse[0] - self.rect.centerx,
            mouse[1] - self.rect.centery,
        )
        self.angle = (180 / math.pi) * -math.atan2(dy, dx)
