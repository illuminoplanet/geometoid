import sys
import pygame

from player import Player
from stage import Stage
from config import *

pygame.init()


screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
)
pygame.display.set_caption("Geometoid")
pygame.font.init()
font = pygame.font.SysFont("Arial", 30)

clock = pygame.time.Clock()


def main():
    stage = Stage(STAGE_PADDING)
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                player.fire = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                player.fire = False
            if event.type == pygame.USEREVENT:
                stage.plan_round()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

        if not paused:
            mouse = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()
            player.update(mouse, keys)
            stage.update(player)

            screen.fill(WHITE)
            stage.draw(screen, font)
            player.draw(screen, font)

            pygame.display.flip()
            clock.tick(FPS)
        else:
            pause_text = font.render("Paused", True, BLACK)
            screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            clock.tick(10)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
