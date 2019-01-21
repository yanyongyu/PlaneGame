# -*- coding:utf-8 -*-
"""
This is the main program of the game.
Author: yanyongyu
"""

__author__ = "yanyongyu"

import sys
import time
import random
import traceback

import pygame
import pygame.locals as gloc

import myplane
import enemy
import bullet
import supply
import boss
import sql

#初始化
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16)
bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('飞机大战')
icon = pygame.image.load('images/icon.gif').convert()
pygame.display.set_icon(icon)
background = pygame.image.load('images/background.png').convert()
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)

#载入音乐，音效
pygame.mixer.music.load('sound/game_music.ogg')
pygame.mixer.music.set_volume(0.2)

bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)

bomb_sound = pygame.mixer.Sound('sound/use_bomb.wav')
bomb_sound.set_volume(0.2)

supply_sound = pygame.mixer.Sound('sound/supply.wav')
supply_sound.set_volume(0.2)

get_bomb_sound = pygame.mixer.Sound('sound/get_bomb.wav')
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound('sound/get_bullet.wav')
get_bullet_sound.set_volume(0.2)

upgrade_sound = pygame.mixer.Sound('sound/upgrade.wav')
upgrade_sound.set_volume(0.2)

enemy3_fly_sound = pygame.mixer.Sound('sound/enemy3_flying.wav')
enemy3_fly_sound.set_volume(0.2)

enemy1_down_sound = pygame.mixer.Sound('sound/enemy1_down.wav')
enemy1_down_sound.set_volume(0.1)
enemy2_down_sound = pygame.mixer.Sound('sound/enemy2_down.wav')
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound('sound/enemy3_down.wav')
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound('sound/me_down.wav')
me_down_sound.set_volume(0.2)

#生成敌方飞机
def add_enemies(fn: pygame.sprite.Sprite,
                num: int,
                *args: pygame.sprite.Group) -> None:
    for i in range(num):
        e = fn(bg_size)
        for group in args:
            if isinstance(group, pygame.sprite.Group):
                group.add(e)
    
#生成子弹            
def init_bullet(fn: pygame.sprite.Sprite,
                num: int,
                *args: tuple) -> list:
    bullet = []
    for i in range(num // len(args)):
        for each in args:
            bullet.append(fn(each, bg_size))
    return bullet

#提升速度
def inc_speed(target: pygame.sprite.Group, inc: int) -> None:
    for each in target:
        each.speed += inc
        
#消灭屏幕中敌方飞机
def kill_enemies(group: pygame.sprite.Group) -> None:
    for each in group:
        if each.rect.bottom > 0:
            each.active = False
            
def change_music(boss: bool=False, play: bool=True) -> None:
    if not boss:
        pygame.mixer.music.load('sound/game_music.ogg')
    else:
        if random.choice([True,False]):
            pygame.mixer.music.load('sound/base.ogg')
        else:
            pygame.mixer.music.load('sound/jungle.ogg')
    if play:
        pygame.mixer.music.play(-1)

#主程序
def main():
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    running = True

    #生成我方飞机
    me = myplane.MyPlane(bg_size)

    #生成敌方飞机
    enemies = pygame.sprite.Group()
    #小型飞机
    small_enemies = pygame.sprite.Group()
    add_enemies(enemy.SmallEnemy, 15, small_enemies, enemies)
    #中型飞机
    mid_enemies = pygame.sprite.Group()
    add_enemies(enemy.MidEnemy, 4, mid_enemies, enemies)
    #大型飞机
    big_enemies = pygame.sprite.Group()
    add_enemies(enemy.BigEnemy, 2, big_enemies, enemies)
    
    #生成boss
    boss_now = None
    boss_group = pygame.sprite.Group()
    boss_lv1 = boss.Boss_lv1(bg_size)
    boss_lv2 = boss.Boss_lv2(bg_size)
    boss_lv3 = boss.Boss_lv3(bg_size)
    boss_group.add(boss_lv1, boss_lv2, boss_lv3)
    
    #生成子弹
    bullets = None
    update = False
    #生成普通子弹
    bullet1_index = 0
    BULLET1_NUM = 4
    bullet1 = init_bullet(bullet.Bullet1, BULLET1_NUM, me.rect.midtop)

    #生成超级子弹
    bullet2_index = 0
    BULLET2_NUM = 8
    bullet2 = init_bullet(
            bullet.Bullet2,
            BULLET2_NUM,
            (me.rect.centerx-33, me.rect.centery),
            (me.rect.centerx+30, me.rect.centery))
        
    #生成升级子弹
    bullet3_index = 0
    BULLET3_NUM = 4
    bullet3 = init_bullet(bullet.Bullet3, BULLET3_NUM, me.rect.midtop)
        
    #生成超级升级子弹
    bullet4_index = 0
    BULLET4_NUM = 8
    bullet4 = init_bullet(
            bullet.Bullet4,
            BULLET4_NUM,
            (me.rect.centerx-33, me.rect.centery),
            (me.rect.centerx+30, me.rect.centery))
    
    #生成boss子弹
    boss_bullet_index = 0
    BOSS_BULLET_NUM = 4
    #生成boss子弹1
    boss_bullet_1 = init_bullet(
            bullet.Boss_bullet_lv1,
            BOSS_BULLET_NUM,
            boss_lv1.rect.midbottom)
    #生成boss子弹2
    boss_bullet_2 = init_bullet(
            bullet.Boss_bullet_lv2,
            BOSS_BULLET_NUM,
            boss_lv2.rect.midbottom)
    #生成boss子弹3
    boss_bullet_3 = init_bullet(
            bullet.Boss_bullet_lv3,
            BOSS_BULLET_NUM,
            boss_lv3.rect.midbottom)

    #等级选项
    level = 1

    #发放补给包
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    bullet_update = supply.Bullet_Update(bg_size)
    medical_supply = supply.Medical_supply(bg_size)
    SUPPLY_TIME = gloc.USEREVENT
    supply_time = time.time()

    #超级子弹定时器
    DOUBLE_BULLET_TIME = gloc.USEREVENT + 1
    is_double = False

    #统计得分
    score = 0
    score_font = pygame.font.Font('font/font.ttf',36)
    record_score = sql.Sql.get_score()

    #读取写入得分选项
    recorded = False

    #暂停选项
    paused = False
    pause_nor_image = pygame.image.load('images/pause_nor.png').convert_alpha()
    pause_pressed_image = pygame.image.load('images/pause_pressed.png').convert_alpha()
    resume_nor_image = pygame.image.load('images/resume_nor.png').convert_alpha()
    resume_pressed_image = pygame.image.load('images/resume_pressed.png').convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image

    #切换图片
    switch_image = True

    #延迟切换
    delay = 100

    #生命条数
    life_num = 3

    #无敌计时器
    INVINCIBLE_TIME = gloc.USEREVENT + 2

    #游戏开始画面
    author_font = pygame.font.Font('font/msyh.ttf',20)
    start_image = pygame.image.load('images/start/start.png').convert_alpha()
    start_rect = start_image.get_rect()
    help_image = pygame.image.load('images/start/help.png').convert_alpha()
    help_rect = help_image.get_rect()
    exit_image = pygame.image.load('images/start/exit.png').convert_alpha()
    exit_rect = exit_image.get_rect()
    start = True
    
    #帮助画面
    _help = False
    
    #过渡画面
    transition = False
    trans_delay = 12
    trans_num = 0
    
    #Boss画面
    boss_lv = 0
    boss_appear = False

    #游戏结束画面
    gameover_font = pygame.font.Font('font/font.ttf',48)
    again_image = pygame.image.load('images/start/again.png').convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load('images/start/gameover.png').convert_alpha()
    gameover_rect = gameover_image.get_rect()

    while running:
        for event in pygame.event.get():
            if event.type == gloc.QUIT:
                pygame.quit()
                sys.exit()

            #发放补给包
            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                pygame.time.set_timer(SUPPLY_TIME, 30000)
                supply_time = time.time()
                if score > 750000:
                    if random.choice([True,False]):
                        if random.choice([True,False]):
                            bomb_supply.reset()
                        else:
                            bullet_supply.reset()
                    else:
                        if random.choice([True,False]):
                            medical_supply.reset()
                        else:
                            bullet_update.reset()
                elif random.choice([True,False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            #超级子弹计时器
            elif event.type == DOUBLE_BULLET_TIME:
                is_double = False
                bullet2 = init_bullet(
                    bullet.Bullet2,
                    BULLET2_NUM,
                    (me.rect.centerx-33, me.rect.centery),
                    (me.rect.centerx+30, me.rect.centery))
                bullet4 = init_bullet(
                    bullet.Bullet4,
                    BULLET4_NUM,
                    (me.rect.centerx-33, me.rect.centery),
                    (me.rect.centerx+30, me.rect.centery))
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

            #检测用户按键
            elif event.type == gloc.KEYDOWN:
                #检测用户使用全屏炸弹
                if event.key == gloc.K_SPACE:
                    if me.bomb_num and (not paused):
                        me.bomb_num -= 1
                        me.bomb_action = True
                        bomb_sound.play()
                        if boss_appear:
                            boss_now.energy -= 30
                        else:
                            kill_enemies(enemies)
                                    
                #检测用户p键暂停
                elif event.key == gloc.K_p:
                    paused = not paused
                    if paused:
                        paused_image = resume_pressed_image
                        paused_time = time.time()
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        paused_image = pause_pressed_image
                        if not start and not _help:
                            pygame.time.set_timer(SUPPLY_TIME, 30000-round((paused_time-supply_time)*1000))
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            #己方飞机无敌计时
            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

            #检测鼠标暂停操作
            elif event.type == gloc.MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        paused_image = resume_pressed_image
                        paused_time = time.time()
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        paused_image = pause_pressed_image
                        if not start and not _help:
                            pygame.time.set_timer(SUPPLY_TIME, 30000-round((paused_time-supply_time)*1000))
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
            elif event.type == gloc.MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image

        #根据用户得分增加难度
        if level == 1 and score > 50000:
            level = 2
            upgrade_sound.play()
            #增加3架小型飞机，2架中型飞机，1架大型飞机
            add_enemies(enemy.SmallEnemy, 3, small_enemies, enemies)
            add_enemies(enemy.MidEnemy, 2, mid_enemies, enemies)
            add_enemies(enemy.BigEnemy, 1, big_enemies, enemies)
            #提升速度
            inc_speed(small_enemies,1)

        elif level == 2 and score > 300000:
            level = 3
            upgrade_sound.play()
            #增加5架小型飞机，3架中型飞机，2架大型飞机
            add_enemies(enemy.SmallEnemy, 5, small_enemies, enemies)
            add_enemies(enemy.MidEnemy, 3, mid_enemies, enemies)
            add_enemies(enemy.BigEnemy, 2, big_enemies, enemies)
            #提升速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)

        elif level == 3 and score > 600000:
            level = 4
            upgrade_sound.play()
            #增加5架小型飞机，3架中型飞机，2架大型飞机
            add_enemies(enemy.SmallEnemy, 5, small_enemies, enemies)
            add_enemies(enemy.MidEnemy, 3, mid_enemies, enemies)
            add_enemies(enemy.BigEnemy, 2, big_enemies, enemies)
            #提升速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)

        elif level == 4 and score > 1000000:
            level = 5
            upgrade_sound.play()
            #增加5架小型飞机，3架中型飞机，2架大型飞机
            add_enemies(enemy.SmallEnemy, 5, small_enemies, enemies)
            add_enemies(enemy.MidEnemy, 3, mid_enemies, enemies)
            add_enemies(enemy.BigEnemy, 2, big_enemies, enemies)
            #提升速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
            
        #根据用户得分出现boss
        if boss_lv == 0 and score > 100000:
            boss_lv = 1
            boss_now = boss_lv1
            boss_bullet = boss_bullet_1
            boss_appear = True
            transition = True
            me.bomb_action = False
            kill_enemies(enemies)
            change_music(True)
        elif boss_lv == 1 and score > 300000:
            boss_lv = 2
            boss_now = boss_lv2
            boss_bullet = boss_bullet_2
            boss_appear = True
            transition = True
            me.bomb_action = False
            kill_enemies(enemies)
            change_music(True)
        elif boss_lv == 2 and score > 750000:
            boss_lv = 3
            boss_now = boss_lv3
            boss_bullet = boss_bullet_3
            boss_appear = True
            transition = True
            me.bomb_action = False
            kill_enemies(enemies)
            change_music(True)

        screen.blit(background,(0,0))
        
## --------------------------------游戏开始画面---------------------------------
        if start and not _help:
            title_image = pygame.image.load('images/start/title.png').convert_alpha()
            title_image_rect = title_image.get_rect()
            title_image_rect.left, title_image_rect.top = (width - title_image_rect.width) // 2, (height // 3) - 40
            screen.blit(title_image, title_image_rect)
            
            start_rect.left, start_rect.top = (width - start_rect.width) // 2, 413
            screen.blit(start_image, start_rect)
            
            help_rect.left, help_rect.top = (width - help_rect.width) // 2, 463
            screen.blit(help_image, help_rect)
            
            exit_rect.left, exit_rect.top = (width - exit_rect.width) // 2, 513
            screen.blit(exit_image, exit_rect)
            
            author_text = author_font.render('directed by : ShowTime--Joker',True,WHITE)
            author_text_rect = author_text.get_rect()
            author_text_rect.left = width - author_text_rect.width - 10
            author_text_rect.top = height - author_text_rect.height - 10
            screen.blit(author_text, author_text_rect)
            
            record_score_text = score_font.render('Best : %d' % record_score, True, WHITE)
            screen.blit(record_score_text, (50,50))
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(pos):
                    start = False
                    if paused:
                        paused = False
                        paused_image = pause_pressed_image
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                    supply_time = time.time()
                    pygame.time.set_timer(SUPPLY_TIME, 30000)
                elif help_rect.collidepoint(pos):
                    _help = True
                elif exit_rect.collidepoint(pos):
                    pygame.quit()
                    sys.exit()
                    
## --------------------------------帮助画面------------------------------------
        elif _help:
            help_image1 = pygame.image.load('images/help/help1.png').convert_alpha()
            help_image2 = pygame.image.load('images/help/help2.png').convert_alpha()
            back_image1 = pygame.image.load('images/help/back1.png').convert_alpha()
            back_image2 = pygame.image.load('images/help/back2.png').convert_alpha()
            if switch_image:
                screen.blit(help_image1, (10,0))
                screen.blit(back_image1, (0,0))
            else:
                screen.blit(help_image2, (10,0))
                screen.blit(back_image2, (0,0))
                
            #切换图片
            if not (delay % 5):
                switch_image = not switch_image
            delay -= 1
            if not delay:
                delay = 100
                
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if back_image1.get_rect().collidepoint(pos):
                    _help = False
        
## --------------------------------背景过渡------------------------------------
        elif transition:
            #毁灭画面中敌方飞机
            enemy3_fly_sound.stop()
            if trans_delay:
                trans_delay -= 1
                for each in enemies:
                    if each.rect.bottom > 0 and (not each.active):
                        screen.blit(each.destroy_images[each.destroy_index],each.rect)
                        if not(trans_delay % 3):
                            each.destroy_index = (each.destroy_index + 1) % 4
                            if each.destroy_index == 0:
                                each.reset()
                #绘制我方飞机
                if me.active:
                    if switch_image:
                        screen.blit(me.image1,me.rect)
                    else:
                        screen.blit(me.image2,me.rect)
                
                #切换图片
                if not (trans_delay % 5):
                    switch_image = not switch_image
            #背景过渡
            else:
                if boss_appear:
                    trans_num += 1
                    screen.blit(boss_now.transitional_image[boss_now.transitional_index],(0,0))
                    if not (trans_num % 4):
                        boss_now.transitional_index = (boss_now.transitional_index + 1) % len(boss_now.transitional_image)
                        if not boss_now.transitional_index:
                            me.init_image()
                            trans_num = 0
                            transition = False
                else:
                    trans_num += 1
                    screen.blit(boss_now.background, (0,0))
                    screen.blit(boss_now.destroy_image[boss_now.destroy_index],(0,0))
                    if not (trans_num % 6):
                        boss_now.destroy_index = (boss_now.destroy_index + 1) % len(boss_now.destroy_image)
                        if not boss_now.destroy_index:
                            me.init_image(True)
                            me.bomb_action = False
                            trans_num = 0
                            trans_delay = 12
                            change_music()
                            transition = False
        
## ------------------------------游戏结束画面-----------------------------------
        elif life_num == 0:
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            pygame.time.set_timer(SUPPLY_TIME, 0)
            if not recorded:
                recorded = True
                if score > record_score:
                    sql.Sql.set_score(score)
                        
            record_score_text = score_font.render('Best : %d' % record_score, True, WHITE)
            screen.blit(record_score_text, (50,50))
            
            gameover_text1 = gameover_font.render('Your Score', True, WHITE)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)
            
            gameover_text2 = gameover_font.render(str(score), True, WHITE)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = (width - gameover_text2_rect.width) // 2, gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)
            
            again_rect.left, again_rect.top = (width - again_rect.width) // 2, gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)
            
            gameover_rect.left, gameover_rect.top = (width - gameover_rect.width) // 2, again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if again_rect.collidepoint(pos):
                    main()
                elif gameover_rect.collidepoint(pos):
                    pygame.quit()
                    sys.exit()
        
        else:
            #boss背景
            if boss_appear:
                screen.blit(boss_now.background,(0,0))
                
            if not paused:
                #检测键盘按键操作
                key_pressed = pygame.key.get_pressed()
                if key_pressed[gloc.K_w] or key_pressed[gloc.K_UP]:
                    me.moveUp()
                if key_pressed[gloc.K_s] or key_pressed[gloc.K_DOWN]:
                    me.moveDown()
                if key_pressed[gloc.K_a] or key_pressed[gloc.K_LEFT]:
                    me.moveLeft()
                if key_pressed[gloc.K_d] or key_pressed[gloc.K_RIGHT]:
                    me.moveRight()
            
            #绘制我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1,me.rect)
                else:
                    screen.blit(me.image2,me.rect)
                if me.invincible:
                    screen.blit(
                            me.shield,
                            (me.rect.centerx - me.shield_rect.width // 2,
                             me.rect.centery - me.shield_rect.height // 2))
            else:
                #毁灭
                if me.destroy_index == 0:
                    me_down_sound.play()
                screen.blit(me.destroy_images[me.destroy_index],me.rect)
                if not(delay % 3):
                    me.destroy_index = (me.destroy_index + 1) % 4
                    if me.destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        update = False
                        pygame.time.set_timer(INVINCIBLE_TIME, 3000)
                        
            #全屏炸弹效果
            if me.bomb_action:
                screen.blit(me.bomb_images[me.bomb_action_index], (0,0))
                if not (delay % 6):
                    me.bomb_action_index = (me.bomb_action_index + 1) % 6
                    if not me.bomb_action_index:
                        me.bomb_action = False
            
            #绘制子弹
            if not (delay % 10) and (not paused):
                bullet_sound.play()
                if is_double:
                    if update:
                        bullets = bullet4
                        bullets[bullet4_index].reset((me.rect.centerx-33,me.rect.centery))
                        bullets[bullet4_index+1].reset((me.rect.centerx+30,me.rect.centery))
                        bullet4_index = (bullet4_index + 2) % BULLET4_NUM
                    else:
                        bullets = bullet2
                        bullets[bullet2_index].reset((me.rect.centerx-33,me.rect.centery))
                        bullets[bullet2_index+1].reset((me.rect.centerx+30,me.rect.centery))
                        bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                else:
                    if update:
                        bullets = bullet3
                        bullets[bullet3_index].reset(me.rect.midtop)
                        bullet3_index = (bullet3_index + 1) % BULLET3_NUM
                    else:
                        bullets = bullet1
                        bullets[bullet1_index].reset(me.rect.midtop)
                        bullet1_index = (bullet1_index + 1) % BULLET1_NUM
            
            #绘制炸弹
            bomb_text = me.bomb_font.render('× %d' % me.bomb_num, True, WHITE)
            screen.blit(me.bomb_image, (10, height - 10 - me.bomb_rect.height))
            screen.blit(bomb_text, (20 + me.bomb_rect.width, height - 10 - me.bomb_rect.height))

            #绘制剩余生命条数
            if life_num:
                for i in range(life_num):
                    screen.blit(me.life_image, \
                                (width-10-(i+1)*me.life_rect.width, \
                                 height-10-me.life_rect.height))
            #绘制得分
            score_text = score_font.render('Score : %s' % str(score), True, WHITE)
            screen.blit(score_text,(10,5))
                
            #绘制全屏炸弹补给包
            if bomb_supply.active and not paused:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply,me):
                    get_bomb_sound.play()
                    if me.bomb_num < 3:
                        me.bomb_num += 1
                    bomb_supply.active = False

            #绘制超级子弹补给包
            if bullet_supply.active and not paused:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    is_double = True
                    bullet1 = init_bullet(bullet.Bullet1, BULLET1_NUM, me.rect.midtop)
                    bullet3 = init_bullet(bullet.Bullet3, BULLET3_NUM, me.rect.midtop)
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18000)
                    bullet_supply.active = False
                    
            #绘制升级子弹补给包
            if bullet_update.active and not paused:
                bullet_update.move()
                screen.blit(bullet_update.image, bullet_update.rect)
                if pygame.sprite.collide_mask(bullet_update, me):
                    get_bullet_sound.play()
                    update = True
                    bullet1 = init_bullet(bullet.Bullet1, BULLET1_NUM, me.rect.midtop)
                    bullet2 = init_bullet(
                        bullet.Bullet2,
                        BULLET2_NUM,
                        (me.rect.centerx-33, me.rect.centery),
                        (me.rect.centerx+30, me.rect.centery))
                    bullet_update.active = False
            
            #绘制医疗包
            if medical_supply.active and not paused:
                medical_supply.move()
                screen.blit(medical_supply.image, medical_supply.rect)
                if pygame.sprite.collide_mask(medical_supply, me):
                    get_bomb_sound.play()
                    if life_num < 3:
                        life_num += 1
                    medical_supply.active = False
                    
            #跟随时间加分
            if not (delay % 60):
                score += 1000

            #切换图片
            if not (delay % 5):
                switch_image = not switch_image
            delay -= 1
            if not delay:
                delay = 100
            
## -------------------------------boss画面-------------------------------------
            if boss_appear and (not paused) and (not transition):
                #检测飞机碰撞
                boss_down = pygame.sprite.spritecollide(me, boss_group, False, pygame.sprite.collide_mask)
                if boss_down and not me.invincible:
                    if boss_now.active:
                        me.active = False
                            
                #绘制boss
                if boss_now.active:
                    boss_now.move_in()
                    boss_now.move()
                    if boss_now.hit:
                        screen.blit(boss_now.image_hit,boss_now.rect)
                        boss_now.hit = False
                    else:
                        screen.blit(boss_now.image,boss_now.rect)
                        
                    #绘制血槽
                    pygame.draw.line(
                            screen,
                            BLACK,
                            (boss_now.rect.left, boss_now.rect.top - 5),
                            (boss_now.rect.right,boss_now.rect.top - 5),
                            4)
                    boss_now_remain = boss_now.energy / boss_now.__class__.energy
                    if boss_now_remain > 0.2:
                        boss_now.energy_color = GREEN
                    else:
                        boss_now.energy_color = RED
                    pygame.draw.line(
                            screen,
                            boss_now.energy_color,
                            (boss_now.rect.left, boss_now.rect.top - 5),
                            (boss_now.rect.left + boss_now.rect.width*boss_now_remain, boss_now.rect.top - 5),
                            4)
                else:
                    for each in boss_bullet:
                        each.active = False
                    if random.choice([True, False]):
                        bullet_update.reset()
                    else:
                        medical_supply.reset()
                    boss_appear = False
                    transition = True
                    
                #boss攻击
                if (not delay % 70) and (boss_now.rect.top >= 53):
                    boss_bullet[boss_bullet_index].reset(
                            (boss_now.rect.centerx + random.randint(-100,40),
                             boss_now.rect.centery)
                        )
                    boss_bullet_index = (boss_bullet_index + 1) % BOSS_BULLET_NUM
                    
                
                #检测是否击中敌机
                for b in bullets:
                    if b.active:
                        b.move()
                        screen.blit(b.image, b.rect)
                        boss_hit = pygame.sprite.spritecollide(b, boss_group, False, pygame.sprite.collide_mask)
                        if boss_hit:
                            b.active = False
                            boss_now.energy -= b.dmg
                            boss_now.hit = True
                            if boss_now.energy <=0:
                                score += boss_now.score
                                boss_now.active = False
                                
                #检测是否被击中
                for b in boss_bullet:
                    if b.active:
                        b.move()
                        screen.blit(b.image, b.rect)
                        boss_bullet_hit = pygame.sprite.collide_mask(b, me)
                        if boss_bullet_hit and not me.invincible:
                            b.active = False
                            me.active = False
                    
## --------------------------------游戏画面------------------------------------
            elif life_num and (not paused):
                #检测飞机碰撞
                enemies_down = pygame.sprite.spritecollide(me, enemies, False,pygame.sprite.collide_mask)
                if enemies_down and not me.invincible:
                    for each in enemies_down:
                        if each.active:
                            me.active = False
                            each.active = False
    
                #绘制敌机
                #大型敌机
                for each in big_enemies:
                    if each.active:
                        each.move()
                        if each.hit:
                            screen.blit(each.image_hit,each.rect)
                            each.hit = False
                        else:
                            if switch_image:
                                screen.blit(each.image1,each.rect)
                            else:
                                screen.blit(each.image2,each.rect)
                        #绘制血槽
                        pygame.draw.line(
                                screen,
                                BLACK,
                                (each.rect.left,each.rect.top - 5),
                                (each.rect.right,each.rect.top - 5),
                                2)
                        big_energy_remain = each.energy / each.__class__.energy
                        if big_energy_remain > 0.2:
                            each.energy_color = GREEN
                        else:
                            each.energy_color = RED
                        pygame.draw.line(
                                screen,
                                each.energy_color,
                                (each.rect.left,each.rect.top - 5),
                                (each.rect.left + each.rect.width*big_energy_remain,each.rect.top - 5),
                                2)
                        
                        #大型提示音效
                        if each.rect.bottom == -50:
                            enemy3_fly_sound.play(-1)
                    else:
                        #毁灭
                        if each.destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[each.destroy_index],each.rect)
                        if not(delay % 3):
                            each.destroy_index = (each.destroy_index + 1) % 6
                            if each.destroy_index == 0:
                                score += each.__class__.score
                                enemy3_fly_sound.stop()
                                each.reset()
                    if each.rect.top == each.height:
                        enemy3_fly_sound.stop()
    
                #中型敌机
                for each in mid_enemies:
                    if each.active:
                        each.move()
                        if each.hit:
                            screen.blit(each.image_hit,each.rect)
                            each.hit = False
                        else:
                            screen.blit(each.image,each.rect)
                        #绘制血槽
                        pygame.draw.line(
                                screen,
                                BLACK,
                                (each.rect.left,each.rect.top - 5),
                                (each.rect.right,each.rect.top - 5),
                                2)
                        mid_energy_remain = each.energy / enemy.MidEnemy.energy
                        if mid_energy_remain > 0.2:
                            each.energy_color = GREEN
                        else:
                            each.energy_color = RED
                        pygame.draw.line(
                                screen,
                                each.energy_color,
                                (each.rect.left,each.rect.top - 5),
                                (each.rect.left + each.rect.width * mid_energy_remain,each.rect.top - 5),
                                2)
                    else:
                        #毁灭
                        if each.destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[each.destroy_index],each.rect)
                        if not(delay % 3):
                            each.destroy_index = (each.destroy_index + 1) % 4
                            if each.destroy_index == 0:
                                score += each.__class__.score
                                each.reset()
    
                #小型敌机
                for each in small_enemies:
                    if each.active:
                        each.move()
                        screen.blit(each.image,each.rect)
                    else:
                        #毁灭
                        if not(delay % 3):
                            if each.destroy_index == 0:
                                enemy1_down_sound.play()
                            screen.blit(each.destroy_images[each.destroy_index],each.rect)
                            each.destroy_index = (each.destroy_index + 1) % 4
                            if each.destroy_index == 0:
                                score += each.__class__.score
                                each.reset()
    
                #检测是否击中敌机
                if bullets:
                    for b in bullets:
                        if b.active:
                            b.move()
                            screen.blit(b.image, b.rect)
                            enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                            if enemy_hit:
                                b.active = False
                                for e in enemy_hit:
                                    if e in mid_enemies or e in big_enemies:
                                        e.hit = True
                                        e.energy -= b.dmg
                                        if e.energy <= 0:
                                            e.active = False
                                    else:
                                        e.active = False

        #绘制暂停按钮
        screen.blit(paused_image,paused_rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
