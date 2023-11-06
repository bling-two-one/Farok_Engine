import pygame

pygame.init()

#색
bg = [38, 50, 54]

#이미지
title_img = pygame.image.load("Image\\Title\\title.png")

#게임 화면
pygame.display.set_caption("Farok_Engine")
size = [1000, 500]
screen = pygame.display.set_mode(size)

#게임 종료 판정
run = True
clock = pygame.time.Clock()

while(True):

    #프레임 제한(현재 30)
    clock.tick(30)

    #타이틀 및 기본 화면 설정
    screen.fill(bg)
    screen.blit(title_img, (size[0]/3, size[1]/3))

    #이벤트 감지
    for event in pygame.event.get(): #유저가 뭔가 함
        if event.type == pygame.QUIT: #유저가 누름 == 무엇
            close=False #무엇 함

    pygame.display.flip()
    
pygame.quit()
