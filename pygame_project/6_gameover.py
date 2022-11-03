#1. 모든 공을 없앨시 게임종료
#2. 캐릭터가 공에 닿을시 게임종료
#3. 시간제한 99초 초과시 게임종료
import os
import pygame
###########################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init() #초기화

# 화면 크기 설정
screen_width=640
screen_height=480
screen=pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("JaeGu Game") 

# FPS
clock = pygame.time.Clock()
############################################################



#1. 사용자 게임 초기화(배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__) # 현재 파일 위치 변환
image_path = os.path.join(current_path, "images") # image 폴더 위치 변환

#배경
background = pygame.image.load(os.path.join(image_path, "background.png"))

#스테이지
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지 높이 위에 캐릭터를 두기 위해 사용

#캐릭터
character=pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width/2 - character_width
character_y_pos = screen_height - stage_height - character_height
character_to_x = 0
character_speed = 5

#무기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

#무기는 여러 발 발사 가능, 리스트로 복사
weapons = []

#무기 이동 속도
weapon_speed = 10

#폰트 정의
game_font = pygame.font.Font(None, 40) # 폰트 객체 생성 (폰트, 크기)

#공 만들기
ball_images = [
    pygame.image.load(os.path.join(image_path, "ballon1.png")),
    pygame.image.load(os.path.join(image_path, "ballon2.png")),
    pygame.image.load(os.path.join(image_path, "ballon3.png")),
    pygame.image.load(os.path.join(image_path, "ballon4.png"))
]

# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9] # index 0, 1, 2, 3 에 해당하는 값

# 공들
balls=[]
balls.append({ 
    "pos_x":50, 
    "pos_y":50, 
    "img_idx":0, 
    "to_x": 3, 
    "to_y": -6, 
    "init_spd_y": ball_speed_y[0] 
})

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

#총 시간
total_time = 30
#시간 
start_ticks = pygame.time.get_ticks() # 현재 tick을 받아옴  
game_result = "Game Over"

running=True
while running:
    dt = clock.tick(30)

    #2. 이벤트 처리 (키보드, 마우스, 등)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + character_width/2 - weapon_width/2
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    #3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x
    if character_x_pos < 0 : 
        character_x_pos = 0 
    elif character_x_pos > screen_width - character_width: 
        character_x_pos = screen_width - character_width 

    # 무기 위치 정의 
    weapons =[[w[0], w[1] - weapon_speed] for w in weapons] 

    #무기 하늘에 닿으면 없어지기 
    weapons =[[w[0], w[1]] for w in weapons if w[1] > 0] 

    # 공 위치 정의 
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 가로 벽에 닿았을 때 튕기는 함수
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * (-1) 

        # 스테이지에 닿았을 때 튕기는 함수
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else: # 그 외의 모든 경우에는 속도를 증가시킴
            ball_val["to_y"] += 0.5
        
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    #4. 충돌 처리

    # 캐릭터 rect 정보 저장
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        # 공 rect 정보 저장
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y
        # 공과 캐릭터 충돌 체크
        if character_rect.colliderect(ball_rect):
            game_result = "Game Over"
            running = False
            break

        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]
            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx

                #가장 작은 크기의 공이 아니라면 공 나눠주기
                if ball_img_idx < 3:
                    #현재 공 크기 정보 가져오기
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    #나눠진 공 크기 정보 가져오기
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    #좌측으로 나눠질 공
                    balls.append({ 
                            "pos_x":ball_pos_x + ball_width/2 - small_ball_width/2, 
                            "pos_y":ball_pos_y + ball_height/2 - small_ball_height/2, 
                            "img_idx":ball_img_idx + 1, 
                            "to_x": -3, 
                            "to_y": -6, 
                            "init_spd_y": ball_speed_y[ball_img_idx + 1] })
                    #우측으로 나눠질 공
                    balls.append({ 
                            "pos_x":ball_pos_x + ball_width/2 - small_ball_width/2, 
                            "pos_y":ball_pos_y + ball_height/2 - small_ball_height/2, 
                            "img_idx":ball_img_idx + 1, 
                            "to_x": 3, 
                            "to_y": -6, 
                            "init_spd_y": ball_speed_y[ball_img_idx + 1] })
                    break
        else: # 계속 게임을 진행
            continue # 안쪽 for문 조건이 맞지않으면 continue
        break # 안쪽 break 조건 성립시 여기로 진입가능
            
            
    # 충돌된 공 or 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 게임 오버
    if not balls:
        game_result = "Game Clear"
        running = False
        #타이머 집어 넣기
    #경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    #경과 시간을 1000으로 나누어서 초 단위로 표시

    timer = game_font.render(str(int(total_time - elapsed_time)), True, (255,255,255))
    #출력할 글자, True, 글자 색상

    #만약 시간이 0 이하이면 게임 종료
    if total_time - elapsed_time <= 0:
        game_result = "Time Out"
        running = False
        
    #5. 화면에 그리기
    screen.blit(background, (0,0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0,screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(timer,(10,10))
    pygame.display.update()

#게임오버 메세지
msg = game_font.render(game_result, True, (0,0,0))
msg_rect = msg.get_rect(center = (int(screen_width/2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()
# 2초 대기
pygame.time.delay(2000)

pygame.quit()