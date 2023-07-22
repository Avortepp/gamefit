import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()
HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 20)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELOW = (255,255,0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player_size = (20, 20)
player = pygame.image.load('player.png').convert_alpha()
player_rect = player.get_rect(center=(WIDTH/4, HEIGHT/2))
player_move_down = [0, 5]
player_move_right = [5, 0] 
player_move_up = [0, -5]
player_move_left = [-5, 0]

def create_bonus():
    bonus_size = (30,30)
    bonus_rect = pygame.Rect(random.randint(0, WIDTH - bonus_size[0]), -bonus_size[1], *bonus_size)
    bonus_move =[0, random.randint(4,8)]
    if random.randint(1,10) == 1:
        bonus_points = 10
        bonus_image = pygame.image.load('bonus10.png').convert_alpha()
    else:
        bonus_points = 1
        bonus_image = pygame.image.load('bonus.png').convert_alpha()
    return [bonus_image, bonus_rect,bonus_move, bonus_points]

def create_enemy():
    enemy_size = (20, 20)
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT - enemy_size[1]), *enemy_size)
    enemy_move = [random.randint(-8,-4), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1 
pygame.time.set_timer(CREATE_ENEMY, 2000)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []

score = 0
image_index = 0
playing = True
paused = False
pause_button = pygame.transform.scale(pygame.image.load('pause_button.png').convert_alpha(), (50, 50))
pause_button_rect = pause_button.get_rect(topright=(WIDTH - 10 - pause_button.get_width() - 10, 10))
pause_text = pygame.font.Font("shrift/float.ttf", 80).render("Пауза", True, COLOR_BLACK)

def draw_game_over_text():
    game_over_text = pygame.font.Font("shrift/float.ttf", 80).render("KIHEЦЬ ГРИ", True, COLOR_BLACK)
    text_rect = game_over_text.get_rect(center=(WIDTH/2, HEIGHT/2))
    main_display.blit(game_over_text, text_rect)

while playing: 
    FPS.tick(260)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index +=1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pause_button_rect.collidepoint(event.pos):
                paused = not paused
              
    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 =bg.get_width()    

    if not paused:
        main_display.blit(bg, (bg_X1,0))
        main_display.blit(bg, (bg_X2,0))
        main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))
        main_display.blit(player, player_rect)
        main_display.blit(pause_button, pause_button_rect) 
    
        keys = pygame.key.get_pressed()

        if keys[K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect = player_rect.move(player_move_down)
        
        if keys[K_UP] and player_rect.top > 0:
            player_rect = player_rect.move(player_move_up)

        if keys[K_RIGHT] and player_rect.right < WIDTH:
            player_rect = player_rect.move(player_move_right)

        if keys[K_LEFT]  and player_rect.left > 0:
            player_rect = player_rect.move(player_move_left)   
        
        for enemy in enemies:
            enemy[1] = enemy[1].move(enemy[2])
            main_display.blit(enemy[0], enemy[1])
        
            if player_rect.colliderect(enemy[1]):
                playing = False

        
        for bonus in bonuses:
            bonus[1] = bonus[1].move(bonus[2])
            main_display.blit(bonus[0],bonus[1])

            if player_rect.colliderect(bonus[1]):
                score += bonus[3]
                bonuses.pop(bonuses.index(bonus))

        main_display.blit(FONT.render(str(score),True, COLOR_BLACK), (WIDTH-50, 20))
        main_display.blit(player, player_rect)

    if paused:
        main_display.blit(pause_button, pause_button_rect)
        pause_text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        main_display.blit(pause_text, pause_text_rect)
           
    pygame.display.flip()
    
    for enemy in enemies:
        if enemy[1].top > HEIGHT:
            enemies.remove(enemy)
    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.remove(bonus)
            
pygame.time.wait(1000)  
draw_game_over_text()
pygame.display.flip()
pygame.time.wait(3000)  

pygame.quit()