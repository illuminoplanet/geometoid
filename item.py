############################
########## phase2 ##########
############################
import math
import pygame

class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.rect = pygame.Rect(x, y, 15, 15)
        self.proj_image = pygame.image.load("assets/proj_enemy.png")

    def update(self):
        raise NotImplementedError
    
    def draw(self, screen):
        raise NotImplementedError

    def check_collision(self, other):
        self_x, self_y = self.x, self.y
        other_x, other_y = other.rect.center
        distance = math.hypot(self_x - other_x, self_y - other_y)
        return distance < self.radius


class Health(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "health")
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

class Damage(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "damage")
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

class Bomb(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "bomb")
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

############################
########## phase2 ##########
############################