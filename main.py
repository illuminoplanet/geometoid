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
    stage = Stage(STAGE_PADDING, screen)
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    running = True
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

        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        screen.fill(WHITE)
        stage.draw(screen, font)
        player.draw(screen, font)

        player.update(mouse, keys)
        stage.update(player)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
