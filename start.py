############################
########## phase2 ##########
############################

import pygame

from config import *

class Start:
    def __init__(self, padding):
        self.padding = padding

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, self.padding))
        pygame.draw.rect(screen, BLACK, (0, 0, self.padding, SCREEN_HEIGHT))
        pygame.draw.rect(
            screen, BLACK, (0, SCREEN_HEIGHT - self.padding, SCREEN_WIDTH, self.padding)
        )
        pygame.draw.rect(
            screen, BLACK, (SCREEN_WIDTH - self.padding, 0, self.padding, SCREEN_HEIGHT)
        )

        text = pygame.font.SysFont("Arial", 50).render("Welcome to Geometoid!", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100))

        text = pygame.font.SysFont("Arial", 25).render("WASD - Move / MOUSELEFT - Shot / ESC - Exit / SPACE - Pause", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT - text.get_height()))

        text = pygame.font.SysFont("Arial", 25).render("Press any key to start..", True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2 + 100))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    waiting = False
                    if event.key == pygame.K_ESCAPE:
                        return False
                    return True

############################
########## phase2 ##########
############################