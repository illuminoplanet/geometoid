import pygame


class Player:
    def __init__(self, x, y, size=50):
        self.rect = pygame.Rect(x, y, size, size)

        self.color = (0, 0, 0)
        self.speed = 5

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
