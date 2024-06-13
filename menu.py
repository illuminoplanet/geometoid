import sys
import pygame
from config import *


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ["Start Game", "Quit"]
        self.selected_option = 0
        self.font = pygame.font.SysFont("Arial", 30)
    def draw(self):
        self.screen.fill(WHITE)
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                color = BLACK
            else:
                color = (100, 100, 100)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 60))
            self.screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:
                    return "start_game"
                elif self.selected_option == 1:
                    pygame.quit()
                    sys.exit()
        return None
