# 심화프로그래밍기말과제, 남한얼, 20240140

import pygame, random

pygame.init()

width = 800
height = 420

background = pygame.display.set_mode((width, height))
pygame.display.set_caption("움치치 움치치")

# 토끼 캐릭터
image_rabbit = pygame.image.load("rabbit.png")
image_rabbit = pygame.transform.scale(image_rabbit, (75, 108) )
rabbit_rect = image_rabbit.get_rect()
rabbit_rect.centerx = (width//2)
rabbit_rect.bottom = (height//2)

# 당근
image_carrat = pygame.image.load("carrat.png")
image_carrat = pygame.transform.scale(image_carrat, (50, 50) )
carrat_rect = image_carrat.get_rect()
carrat_rect.centerx = (width//2)
carrat_rect.bottom = (0)

# 돌
image_rock = pygame.image.load("rock.png")
image_rock = pygame.transform.scale(image_rock, (50, 50))
rock_rect = image_rock.get_rect()
rock_rect.centerx = (width + 50)
rock_rect.bottom = (height)

# 배경
image_bg = pygame.image.load("forest.png")
image_bg = pygame.transform.scale(image_bg, (width, height) )  
bg_wd = image_bg.get_size()[0]
bg_ht = image_bg.get_size()[1]

fps = pygame.time.Clock()

y_vel = 0

# 텍스트
font = pygame.font.SysFont('verdanai', 30)
game_score = 0
text1_score = font.render("Score: " + str(game_score), True, (0,0,0))
text1_score_rect = text1_score.get_rect()
text1_score_rect.topleft = (10, 10)

live_score = 5
text2_score = font.render("Lives: " + str(live_score), True, (0,0,0))
text2_score_rect = text2_score.get_rect()
text2_score_rect.topleft = (10, 30)

# 사운드
pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -16, 2, 512)

# 사운드 파일
jump_sd = pygame.mixer.Sound('jump.mp3')
item_sd = pygame.mixer.Sound('item.mp3')
item_sd.set_volume(0.5)
hit_sd = pygame.mixer.Sound('hit.mp3')
hit_sd.set_volume(0.5)

# 게임 시작 함수
def game_start():
    Sscreen = pygame.display.set_mode((800, 420))

    pygame.font.init()
    Sfont = pygame.font.SysFont("Sans", 50)
    Sfont_OB = font.render("PRESS SPACE KEY TO START THE GAME", True, (255,255,255))
    Sfont_OB_rect = Sfont_OB.get_rect()
    Sfont_OB_rect.center = ((width//2, height//2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return
        Sscreen.fill((0,0,0))
        Sscreen.blit(Sfont_OB, Sfont_OB_rect)
        pygame.display.update()

game_start() 

# 게임 재시작(종료) 함수
def game_restart():
    Rscreen = pygame.display.set_mode((800, 420))

    pygame.font.init()
    font = pygame.font.SysFont("Sans", 50)
    Rfont1_OB = font.render("PRESS SPACE KEY TO RESTART", True, (255,255,255))
    Rfont1_OB_rect = Rfont1_OB.get_rect()
    Rfont1_OB_rect.center = ((width//2, height//2))
    Rfont2_OB = font.render("GAMEOVER", True, (255,0,0))
    Rfont2_OB_rect = Rfont2_OB.get_rect()
    Rfont2_OB_rect.center = ((width//2, height//2 + 50))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                y_vel = 0
                game_score = 0
                live_score = 5
                background = pygame.display.set_mode((width, height))
                play = True
                while play:
                    deltaTime = fps.tick(60)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            play = False
                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_DOWN] and rabbit_rect.bottom < height or keys[pygame.K_s] and rabbit_rect.bottom < height:
                        rabbit_rect.y += 5
                    if keys[pygame.K_RIGHT] and rabbit_rect.right <= width or keys[pygame.K_d] and rabbit_rect.right <= width :
                        rabbit_rect.x += 5
                    if keys[pygame.K_LEFT] and rabbit_rect.left >= 0 or keys[pygame.K_a] and rabbit_rect.left >= 0:
                        rabbit_rect.x -= 5
                        
                    #점프
                    rabbit_rect.top += y_vel
                    y_vel += 1

                    if rabbit_rect.bottom >= height:
                        y_vel = 0
                        if keys[pygame.K_UP] or keys[pygame.K_w]:
                            y_vel = -18
                            jump_sd.play()

                    # 당근
                    if carrat_rect.y > height:
                        carrat_rect.y = height - 450
                        carrat_rect.x = random.randint(50, width - 50)
                    else:
                        carrat_rect.y += 5

                    if rabbit_rect.colliderect(carrat_rect):
                        item_sd.play()
                        carrat_rect.y = height - 450
                        carrat_rect.x = random.randint(50, width - 50)
                        game_score += 1

                    # 돌
                    if rock_rect.x < 0:
                        rock_rect.x = width - 50
                        rock_rect.y = random.randint(200, height-50)
                    else:
                        rock_rect.x -= 10

                    if rabbit_rect.colliderect(rock_rect):
                        hit_sd.play()
                        rock_rect.x = width - 50
                        rock_rect.y = random.randint(200, height-50)
                        live_score -= 1

                    text1_score = font.render("Score:" + str(game_score), True, (0,0,0))

                    if live_score > 0:
                        text2_score = font.render("Lives: " + str(live_score), True, (0,0,0))
                    else:
                        text2_score = font.render("Game Over", True, (255,0,0))
                        game_restart()

                    background.blit(image_bg, (0, 0))
                    background.blit(image_rabbit, rabbit_rect)
                    background.blit(image_carrat, carrat_rect)
                    background.blit(image_rock, rock_rect)
                    background.blit(text1_score, text1_score_rect)
                    background.blit(text2_score, text2_score_rect)
                    pygame.display.update()

                pygame.quit()
                    
        Rscreen.fill((0,0,0))
        Rscreen.blit(Rfont1_OB, Rfont1_OB_rect)
        Rscreen.blit(Rfont2_OB, Rfont2_OB_rect)
        pygame.display.update()

# 게임 코드
play = True
while play:
    deltaTime = fps.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_DOWN] and rabbit_rect.bottom < height or keys[pygame.K_s] and rabbit_rect.bottom < height:
        rabbit_rect.y += 5
    if keys[pygame.K_RIGHT] and rabbit_rect.right <= width or keys[pygame.K_d] and rabbit_rect.right <= width :
        rabbit_rect.x += 5
    if keys[pygame.K_LEFT] and rabbit_rect.left >= 0 or keys[pygame.K_a] and rabbit_rect.left >= 0:
        rabbit_rect.x -= 5
        
    #점프
    rabbit_rect.top += y_vel
    y_vel += 1

    if rabbit_rect.bottom >= height:
        y_vel = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            y_vel = -18
            jump_sd.play()

     # 당근
    if carrat_rect.y > height:
        carrat_rect.y = height - 450
        carrat_rect.x = random.randint(50, width - 50)
    else:
        carrat_rect.y += 5

    if rabbit_rect.colliderect(carrat_rect):
        item_sd.play()
        carrat_rect.y = height - 450
        carrat_rect.x = random.randint(50, width - 50)
        game_score += 1

    # 돌
    if rock_rect.x < 0:
        rock_rect.x = width - 50
        rock_rect.y = random.randint(200, height-50)
    else:
        rock_rect.x -= 10

    if rabbit_rect.colliderect(rock_rect):
        hit_sd.play()
        rock_rect.x = width - 50
        rock_rect.y = random.randint(200, height-50)
        live_score -= 1

    text1_score = font.render("Score:" + str(game_score), True, (0,0,0))

    if live_score > 0:
        text2_score = font.render("Lives: " + str(live_score), True, (0,0,0))
    else:
        text2_score = font.render("Game Over", True, (255,0,0))
        game_restart()

    background.blit(image_bg, (0, 0))
    background.blit(image_rabbit, rabbit_rect)
    background.blit(image_carrat, carrat_rect)
    background.blit(image_rock, rock_rect)
    background.blit(text1_score, text1_score_rect)
    background.blit(text2_score, text2_score_rect)
    pygame.display.update()

pygame.quit()