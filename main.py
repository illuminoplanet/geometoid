import sys
import pygame

from player import Player
from stage import Stage
from config import *
from menu import Menu

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
    menu = Menu(screen)

    running = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if running == True:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    player.fire = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    player.fire = False
                if event.type == pygame.USEREVENT:
                    stage.plan_round()
            else:
                action = menu.handle_event(event)
                if action == "start_game":
                    running = True
                
        if running == True:
            mouse = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()

            screen.fill(WHITE)

            player.update(mouse, keys)
            stage.update(player)
            
            stage.draw(screen, font)
            player.draw(screen, font)

        else: menu.draw()

        pygame.display.flip()
        clock.tick(FPS)



if __name__ == "__main__":
    main()
