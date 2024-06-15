import sys
import pygame

from start import Start
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

    ############################
    ########## phase2 ##########
    ############################
    start = Start(STAGE_PADDING)
    pause = False

    screen.fill(WHITE)
    running = start.draw(screen)
    ############################
    ########## phase2 ##########
    ############################
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

            ############################
            ########## phase2 ##########
            ############################
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                pause = not pause
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False
            ############################
            ########## phase2 ##########
            ############################

        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        ############################
        ########## phase2 ##########
        ############################
        if not pause:
            player.update(mouse, keys)
            if player.health <= 0:
                running = False
                text = font.render("Game Over", True, BLACK)
                screen.blit(
                    text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2)
                )
                pygame.display.flip()
                over = False
                while not over:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYUP:
                            over = True
                break
                
            stage.update(player)

            screen.fill(WHITE)
            stage.draw(screen, font)
            player.draw(screen, font)
        else:
            screen.fill(WHITE)
            text = font.render("Paused", True, BLACK)
            screen.blit(
                text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2)
            )
        ############################
        ########## phase2 ##########
        ############################

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
