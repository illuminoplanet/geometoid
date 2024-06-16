############################
########## phase2 ##########
############################
import math
import pygame

class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.used = False

        self.radius = 15
        self.rect = pygame.Rect(x, y, 15, 15)
        self.proj_image = pygame.image.load("assets/heart.png")
    
    def draw(self, screen):
        raise NotImplementedError

    def check_collision(self, other):
        self_x, self_y = self.x, self.y
        other_x, other_y = other.rect.center
        distance = math.hypot(self_x - other_x, self_y - other_y)
        return distance < self.radius


class Health(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.transform.scale(
            pygame.image.load("assets/heart.png"), (40, 40)
        )
        self.radius = 40
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        new_image = pygame.transform.rotate(
            self.image,
            pygame.time.get_ticks() // 10,
        )
        new_rect = new_image.get_rect(center=(self.x, self.y))
        screen.blit(new_image, new_rect.topleft)

class Shot_Speed(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.transform.scale(
            pygame.image.load("assets/bullet.png"), (30, 40)
        )
        self.radius = 40
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        new_image = pygame.transform.rotate(
            self.image,
            pygame.time.get_ticks() // 10,
        )
        new_rect = new_image.get_rect(center=(self.x, self.y))
        screen.blit(new_image, new_rect.topleft)

class Magazine(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.transform.scale(
            pygame.image.load("assets/magazine.png"), (30, 40)
        )
        self.radius = 40
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        new_image = pygame.transform.rotate(
            self.image,
            pygame.time.get_ticks() // 10,
        )
        new_rect = new_image.get_rect(center=(self.x, self.y))
        screen.blit(new_image, new_rect.topleft)

class Bomb(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.transform.scale(
            pygame.image.load("assets/bomb.png"), (40, 40)
        )
        self.radius = 40
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        pass

    def draw(self, screen):
        new_image = pygame.transform.rotate(
            self.image,
            pygame.time.get_ticks() // 10,
        )
        new_rect = new_image.get_rect(center=(self.x, self.y))
        screen.blit(new_image, new_rect.topleft)

############################
########## phase2 ##########
############################