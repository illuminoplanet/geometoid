import pygame
import sys

from player import Player
from stage import Stage
from config import *

pygame.init()


screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
)
pygame.display.set_caption("Geometoid")

clock = pygame.time.Clock()


def main():
    stage = Stage(STAGE_PADDING)
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        player.move(mouse, keys)

        screen.fill(WHITE)
        stage.draw(screen)
        player.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
