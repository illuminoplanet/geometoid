# https://github.com/Seowonryeol/geometoid - 단순 슈팅 게임.

# 1. 30초 채워서 필살기 가동 - 사방팔방으로 다 발사하기
# 2. 각 오브젝트 위에 체력 표시 및 내 체력 표시 #완료
# 3. 보스 스테이지
# 4. 효과음 추가

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
        player.update(mouse, keys)
        stage.update(player)

        screen.fill(WHITE)
        stage.draw(screen, font)
        player.draw(screen, font)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
