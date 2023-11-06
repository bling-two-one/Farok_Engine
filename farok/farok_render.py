import pygame
import sys

pygame.init()

#색
bg = [38, 50, 54]

#이미지
title_img = pygame.image.load("Image\\image\\title.png")
title_img = pygame.transform.scale(title_img, (800, 140))

#게임 화면
pygame.display.set_caption("Farok_Engine")
size = [1000, 600]
screen = pygame.display.set_mode(size)

#게임 종료 판정
run = True

clock = pygame.time.Clock()

while True:

    #프레임 제한(현재 30)
    clock.tick(30)

    #타이틀 및 기본 화면 설정
    screen.fill(bg)
    screen.blit(title_img, (100, 200))

    #이벤트 감지
    for event in pygame.event.get(): #유저가 뭔가 함
        if event.type == pygame.QUIT: #유저가 누름 == 무엇
            pygame.quit()
            sys.exit()
            

    pygame.display.update()

