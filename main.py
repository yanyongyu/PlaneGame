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

import enemy
import bullet
import supply
import sql
import variables as var

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

#提升速度
def inc_speed(target: pygame.sprite.Group, inc: int) -> None:
    for each in target:
        each.speed += inc
        
#消灭屏幕中敌方飞机
def kill_enemies(group: pygame.sprite.Group) -> None:
    for each in group:
        if each.rect.bottom > 0:
            each.active = False

#主程序
def main():
    init_thread = var.Initializer()
    init_thread.daemon = True
    init_thread.start()
    clock = pygame.time.Clock()
    running = True
    var.init()

    #发放补给包
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    bullet_update = supply.Bullet_Update(bg_size)
    medical_supply = supply.Medical_supply(bg_size)
    SUPPLY_TIME = gloc.USEREVENT

    #超级子弹定时器
    DOUBLE_BULLET_TIME = gloc.USEREVENT + 1

    #统计得分
    score_font = pygame.font.Font('font/font.ttf',36)

    #暂停选项
    pause_nor_image = pygame.image.load('images/pause_nor.png').convert_alpha()
    pause_pressed_image = pygame.image.load('images/pause_pressed.png').convert_alpha()
    resume_nor_image = pygame.image.load('images/resume_nor.png').convert_alpha()
    resume_pressed_image = pygame.image.load('images/resume_pressed.png').convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image
    pause_restart = pygame.image.load('images/restart.png').convert_alpha()
    pause_restart_rect = pause_restart.get_rect()
    pause_restart_rect.left, pause_restart_rect.top = 130, 300
    pause_quit = pygame.image.load('images/quit.png').convert_alpha()
    pause_quit_rect = pause_quit.get_rect()
    pause_quit_rect.left, pause_quit_rect.top = 310, 300

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
                var.supply_time = time.time()
                if var.score > 750000:
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
                var.is_double = False
                var.bullet2 = var.init_bullet(
                    bullet.Bullet2,
                    var.BULLET2_NUM,
                    (var.me.rect.centerx-33, var.me.rect.centery),
                    (var.me.rect.centerx+30, var.me.rect.centery))
                var.bullet4 = var.init_bullet(
                    bullet.Bullet4,
                    var.BULLET4_NUM,
                    (var.me.rect.centerx-33, var.me.rect.centery),
                    (var.me.rect.centerx+30, var.me.rect.centery))
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

            #检测用户按键
            elif event.type == gloc.KEYDOWN:
                #检测用户使用全屏炸弹
                if event.key == gloc.K_SPACE:
                    if var.me.bomb_num and (not var.paused):
                        var.me.bomb_num -= 1
                        var.me.bomb_action = True
                        bomb_sound.play()
                        if var.boss_appear:
                            var.boss_now.energy -= 30
                            for each in var.boss_bullet:
                                each.active = False
                        else:
                            kill_enemies(var.enemies)
                                    
                #检测用户p键暂停
                elif event.key == gloc.K_p or event.key == gloc.K_ESCAPE:
                    var.paused = not var.paused
                    if var.paused:
                        paused_image = resume_pressed_image
                        paused_time = time.time()
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        paused_image = pause_pressed_image
                        if not var.start and not var._help:
                            pygame.time.set_timer(SUPPLY_TIME, 30000-round((paused_time-var.supply_time)*1000))
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            #己方飞机无敌计时
            elif event.type == INVINCIBLE_TIME:
                var.me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

            #检测鼠标暂停操作
            elif event.type == gloc.MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    var.paused = not var.paused
                    if var.paused:
                        paused_image = resume_pressed_image
                        paused_time = time.time()
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        paused_image = pause_pressed_image
                        if not var.start and not var._help:
                            pygame.time.set_timer(SUPPLY_TIME, 30000-round((paused_time-var.supply_time)*1000))
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
            elif event.type == gloc.MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if var.paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if var.paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image

        #根据用户得分增加难度
        if var.level == 1 and var.score > 50000:
            var.level = 2
            upgrade_sound.play()
            #增加3架小型飞机，2架中型飞机，1架大型飞机
            var.add_enemies(enemy.SmallEnemy, 3, var.small_enemies, var.enemies)
            var.add_enemies(enemy.MidEnemy, 2, var.mid_enemies, var.enemies)
            var.add_enemies(enemy.BigEnemy, 1, var.big_enemies, var.enemies)
            #提升速度
            inc_speed(var.small_enemies, 1)

        elif var.level == 2 and var.score > 300000:
            var.level = 3
            upgrade_sound.play()
            #增加5架小型飞机，3架中型飞机，2架大型飞机
            var.add_enemies(enemy.SmallEnemy, 5, var.small_enemies, var.enemies)
            var.add_enemies(enemy.MidEnemy, 3, var.mid_enemies, var.enemies)
            var.add_enemies(enemy.BigEnemy, 2, var.big_enemies, var.enemies)
            #提升速度
            inc_speed(var.small_enemies, 1)
            inc_speed(var.mid_enemies, 1)

        elif var.level == 3 and var.score > 600000:
            var.level = 4
            upgrade_sound.play()
            #增加5架小型飞机，3架中型飞机，2架大型飞机
            var.add_enemies(enemy.SmallEnemy, 5, var.small_enemies, var.enemies)
            var.add_enemies(enemy.MidEnemy, 3, var.mid_enemies, var.enemies)
            var.add_enemies(enemy.BigEnemy, 2, var.big_enemies, var.enemies)
            #提升速度
            inc_speed(var.small_enemies, 1)
            inc_speed(var.mid_enemies, 1)

        elif var.level == 4 and var.score > 1000000:
            var.level = 5
            upgrade_sound.play()
            #增加5架小型飞机，3架中型飞机，2架大型飞机
            var.add_enemies(enemy.SmallEnemy, 5, var.small_enemies, var.enemies)
            var.add_enemies(enemy.MidEnemy, 3, var.mid_enemies, var.enemies)
            var.add_enemies(enemy.BigEnemy, 2, var.big_enemies, var.enemies)
            #提升速度
            inc_speed(var.small_enemies, 1)
            inc_speed(var.mid_enemies, 1)
            
        #根据用户得分出现boss
        if var.boss_lv == 0 and var.score > 100000:
            var.boss_lv = 1
            var.boss_now = var.boss_lv1
            var.boss_bullet = var.boss_bullet_1
            var.boss_appear = True
            var.transition = True
            var.me.bomb_action = False
            kill_enemies(var.enemies)
            var.change_music(True)
        elif var.boss_lv == 1 and var.score > 350000:
            var.boss_lv = 2
            var.boss_now = var.boss_lv2
            var.boss_bullet = var.boss_bullet_2
            var.boss_appear = True
            var.transition = True
            var.me.bomb_action = False
            kill_enemies(var.enemies)
            var.change_music(True)
        elif var.boss_lv == 2 and var.score > 750000:
            var.boss_lv = 3
            var.boss_now = var.boss_lv3
            var.boss_bullet = var.boss_bullet_3
            var.boss_appear = True
            var.transition = True
            var.me.bomb_action = False
            kill_enemies(var.enemies)
            var.change_music(True)

        screen.blit(background,(0,0))
        
## --------------------------------游戏开始画面---------------------------------
        if var.start and not var._help:
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
            
            record_score_text = score_font.render('Best : %d' % var.record_score, True, WHITE)
            screen.blit(record_score_text, (50,50))
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(pos):
                    var.start = False
                    if var.paused:
                        var.paused = False
                        paused_image = pause_pressed_image
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                    var.supply_time = time.time()
                    pygame.time.set_timer(SUPPLY_TIME, 30000)
                elif help_rect.collidepoint(pos):
                    var._help = True
                elif exit_rect.collidepoint(pos):
                    pygame.quit()
                    sys.exit()
                    
## --------------------------------帮助画面------------------------------------
        elif var._help:
            help_image1 = pygame.image.load('images/help/help1.png').convert_alpha()
            help_image2 = pygame.image.load('images/help/help2.png').convert_alpha()
            back_image1 = pygame.image.load('images/help/back1.png').convert_alpha()
            back_image2 = pygame.image.load('images/help/back2.png').convert_alpha()
            if var.switch_image:
                screen.blit(help_image1, (10,0))
                screen.blit(back_image1, (0,0))
            else:
                screen.blit(help_image2, (10,0))
                screen.blit(back_image2, (0,0))
                
            #切换图片
            if not (var.delay % 5):
                var.switch_image = not var.switch_image
            var.delay -= 1
            if not var.delay:
                var.delay = 100
                
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if back_image1.get_rect().collidepoint(pos):
                    var._help = False
        
## --------------------------------背景过渡------------------------------------
        elif var.transition:
            #毁灭画面中敌方飞机
            enemy3_fly_sound.stop()
            if var.trans_delay:
                var.trans_delay -= 1
                for each in var.enemies:
                    if each.rect.bottom > 0 and (not each.active):
                        screen.blit(each.destroy_images[each.destroy_index],each.rect)
                        if not(var.trans_delay % 3):
                            each.destroy_index = (each.destroy_index + 1) % 4
                            if each.destroy_index == 0:
                                each.reset()
                #绘制我方飞机
                if var.me.active:
                    if var.switch_image:
                        screen.blit(var.me.image1, var.me.rect)
                    else:
                        screen.blit(var.me.image2, var.me.rect)
                
                #切换图片
                if not (var.trans_delay % 5):
                    var.switch_image = not var.switch_image
            #背景过渡
            else:
                if var.boss_appear:
                    var.trans_num += 1
                    screen.blit(var.boss_now.transitional_image[var.boss_now.transitional_index],(0,0))
                    if not (var.trans_num % 4):
                        var.boss_now.transitional_index = (var.boss_now.transitional_index + 1) % len(var.boss_now.transitional_image)
                        if not var.boss_now.transitional_index:
                            var.me.init_image()
                            var.trans_num = 0
                            var.transition = False
                else:
                    var.trans_num += 1
                    screen.blit(var.boss_now.background, (0,0))
                    screen.blit(var.boss_now.destroy_image[var.boss_now.destroy_index],(0,0))
                    if not (var.trans_num % 6):
                        var.boss_now.destroy_index = (var.boss_now.destroy_index + 1) % len(var.boss_now.destroy_image)
                        if not var.boss_now.destroy_index:
                            var.me.init_image(True)
                            var.me.bomb_action = False
                            var.trans_num = 0
                            var.trans_delay = 12
                            var.change_music()
                            var.transition = False
        
## ------------------------------游戏结束画面-----------------------------------
        elif var.life_num == 0:
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            pygame.time.set_timer(SUPPLY_TIME, 0)
            if not var.recorded:
                var.recorded = True
                if var.score > var.record_score:
                    sql.Sql.set_score(var.score)
                        
            record_score_text = score_font.render('Best : %d' % var.record_score, True, WHITE)
            screen.blit(record_score_text, (50,50))
            
            gameover_text1 = gameover_font.render('Your Score', True, WHITE)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)
            
            gameover_text2 = gameover_font.render(str(var.score), True, WHITE)
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
                    init_thread = var.Initializer()
                    init_thread.daemon = True
                    init_thread.start()
                    var.init()
                elif gameover_rect.collidepoint(pos):
                    pygame.quit()
                    sys.exit()
## ----------------------------------------------------------------------------
        else:
            #boss背景
            if var.boss_appear:
                screen.blit(var.boss_now.background,(0,0))
                
            #暂停界面
            if var.paused:
                screen.blit(pause_restart, pause_restart_rect)
                screen.blit(pause_quit, pause_quit_rect)
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if pause_restart_rect.collidepoint(pos):
                        init_thread = var.Initializer()
                        init_thread.daemon = True
                        init_thread.start()
                        var.init()
                    elif pause_quit_rect.collidepoint(pos):
                        var.life_num = 0
                
            if not var.paused:
                #检测键盘按键操作
                key_pressed = pygame.key.get_pressed()
                if key_pressed[gloc.K_w] or key_pressed[gloc.K_UP]:
                    var.me.moveUp()
                if key_pressed[gloc.K_s] or key_pressed[gloc.K_DOWN]:
                    var.me.moveDown()
                if key_pressed[gloc.K_a] or key_pressed[gloc.K_LEFT]:
                    var.me.moveLeft()
                if key_pressed[gloc.K_d] or key_pressed[gloc.K_RIGHT]:
                    var.me.moveRight()
            
            #绘制我方飞机
            if var.me.active:
                if var.switch_image:
                    screen.blit(var.me.image1,var.me.rect)
                else:
                    screen.blit(var.me.image2,var.me.rect)
                if var.me.invincible:
                    screen.blit(
                            var.me.shield,
                            (var.me.rect.centerx - var.me.shield_rect.width // 2,
                             var.me.rect.centery - var.me.shield_rect.height // 2))
            else:
                #毁灭
                if var.me.destroy_index == 0:
                    me_down_sound.play()
                screen.blit(var.me.destroy_images[var.me.destroy_index],var.me.rect)
                if not(var.delay % 3):
                    var.me.destroy_index = (var.me.destroy_index + 1) % 4
                    if var.me.destroy_index == 0:
                        var.life_num -= 1
                        var.me.reset()
                        var.update = False
                        pygame.time.set_timer(INVINCIBLE_TIME, 3000)
                        
            #全屏炸弹效果
            if var.me.bomb_action:
                screen.blit(var.me.bomb_images[var.me.bomb_action_index], (0,0))
                if not (var.delay % 6):
                    var.me.bomb_action_index = (var.me.bomb_action_index + 1) % 6
                    if not var.me.bomb_action_index:
                        var.me.bomb_action = False
            
            #绘制子弹
            if not (var.delay % 10) and (not var.paused):
                bullet_sound.play()
                if var.is_double:
                    if var.update:
                        var.bullets = var.bullet4
                        var.bullets[var.bullet4_index].reset((var.me.rect.centerx-33,var.me.rect.centery))
                        var.bullets[var.bullet4_index+1].reset((var.me.rect.centerx+30,var.me.rect.centery))
                        var.bullet4_index = (var.bullet4_index + 2) % var.BULLET4_NUM
                    else:
                        var.bullets = var.bullet2
                        var.bullets[var.bullet2_index].reset((var.me.rect.centerx-33,var.me.rect.centery))
                        var.bullets[var.bullet2_index+1].reset((var.me.rect.centerx+30,var.me.rect.centery))
                        var.bullet2_index = (var.bullet2_index + 2) % var.BULLET2_NUM
                else:
                    if var.update:
                        var.bullets = var.bullet3
                        var.bullets[var.bullet3_index].reset(var.me.rect.midtop)
                        var.bullet3_index = (var.bullet3_index + 1) % var.BULLET3_NUM
                    else:
                        var.bullets = var.bullet1
                        var.bullets[var.bullet1_index].reset(var.me.rect.midtop)
                        var.bullet1_index = (var.bullet1_index + 1) % var.BULLET1_NUM
            
            #绘制炸弹
            bomb_text = var.me.bomb_font.render('× %d' % var.me.bomb_num, True, WHITE)
            screen.blit(var.me.bomb_image, (10, height - 10 - var.me.bomb_rect.height))
            screen.blit(bomb_text, (20 + var.me.bomb_rect.width, height - 10 - var.me.bomb_rect.height))

            #绘制剩余生命条数
            if var.life_num:
                for i in range(var.life_num):
                    screen.blit(var.me.life_image, \
                                (width-10-(i+1)*var.me.life_rect.width, \
                                 height-10-var.me.life_rect.height))
            #绘制得分
            score_text = score_font.render('Score : %s' % str(var.score), True, WHITE)
            screen.blit(score_text,(10,5))
                
            #绘制全屏炸弹补给包
            if bomb_supply.active and not var.paused:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, var.me):
                    get_bomb_sound.play()
                    if var.me.bomb_num < 3:
                        var.me.bomb_num += 1
                    bomb_supply.active = False

            #绘制超级子弹补给包
            if bullet_supply.active and not var.paused:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, var.me):
                    get_bullet_sound.play()
                    var.is_double = True
                    var.bullet1 = var.init_bullet(bullet.Bullet1, var.BULLET1_NUM, var.me.rect.midtop)
                    var.bullet3 = var.init_bullet(bullet.Bullet3, var.BULLET3_NUM, var.me.rect.midtop)
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, 18000)
                    bullet_supply.active = False
                    
            #绘制升级子弹补给包
            if bullet_update.active and not var.paused:
                bullet_update.move()
                screen.blit(bullet_update.image, bullet_update.rect)
                if pygame.sprite.collide_mask(bullet_update, var.me):
                    get_bullet_sound.play()
                    var.update = True
                    var.bullet1 = var.init_bullet(bullet.Bullet1, var.BULLET1_NUM, var.me.rect.midtop)
                    var.bullet2 = var.init_bullet(
                        bullet.Bullet2,
                        var.BULLET2_NUM,
                        (var.me.rect.centerx-33, var.me.rect.centery),
                        (var.me.rect.centerx+30, var.me.rect.centery))
                    bullet_update.active = False
            
            #绘制医疗包
            if medical_supply.active and not var.paused:
                medical_supply.move()
                screen.blit(medical_supply.image, medical_supply.rect)
                if pygame.sprite.collide_mask(medical_supply, var.me):
                    get_bomb_sound.play()
                    if var.life_num < 3:
                        var.life_num += 1
                    medical_supply.active = False
                    
            #跟随时间加分
            if not (var.delay % 60) and not var.paused:
                var.score += 1000

            #切换图片
            if not (var.delay % 5) and not var.paused:
                var.switch_image = not var.switch_image
                
            var.delay -= 1
            if not var.delay:
                var.delay = 100
            
## -------------------------------boss画面-------------------------------------
            if var.boss_appear and (not var.paused) and (not var.transition):
                #检测飞机碰撞
                boss_down = pygame.sprite.spritecollide(var.me, var.boss_group, False, pygame.sprite.collide_mask)
                if boss_down and not var.me.invincible:
                    if var.boss_now.active:
                        var.me.active = False
                            
                #绘制boss
                if var.boss_now.active:
                    var.boss_now.move_in()
                    var.boss_now.move()
                    if var.boss_now.hit:
                        screen.blit(var.boss_now.image_hit,var.boss_now.rect)
                        var.boss_now.hit = False
                    else:
                        screen.blit(var.boss_now.image,var.boss_now.rect)
                        
                    #绘制血槽
                    pygame.draw.line(
                            screen,
                            BLACK,
                            (var.boss_now.rect.left, var.boss_now.rect.top - 5),
                            (var.boss_now.rect.right,var.boss_now.rect.top - 5),
                            4)
                    boss_now_remain = var.boss_now.energy / var.boss_now.__class__.energy
                    if boss_now_remain > 0.2:
                        var.boss_now.energy_color = GREEN
                    else:
                        var.boss_now.energy_color = RED
                    pygame.draw.line(
                            screen,
                            var.boss_now.energy_color,
                            (var.boss_now.rect.left, var.boss_now.rect.top - 5),
                            (var.boss_now.rect.left + var.boss_now.rect.width*boss_now_remain, var.boss_now.rect.top - 5),
                            4)
                else:
                    for each in var.boss_bullet:
                        each.active = False
                    if random.choice([True, False]):
                        bullet_update.reset()
                    else:
                        medical_supply.reset()
                    var.boss_appear = False
                    var.transition = True
                    
                #boss攻击
                if (not var.delay % 70) and (var.boss_now.rect.top >= 53):
                    var.boss_bullet[var.boss_bullet_index].reset(
                            (var.boss_now.rect.centerx + random.randint(-100,40),
                             var.boss_now.rect.centery)
                        )
                    var.boss_bullet_index = (var.boss_bullet_index + 1) % var.BOSS_BULLET_NUM
                    
                
                #检测是否击中敌机
                for b in var.bullets:
                    if b.active:
                        b.move()
                        screen.blit(b.image, b.rect)
                        boss_hit = pygame.sprite.spritecollide(b, var.boss_group, False, pygame.sprite.collide_mask)
                        if boss_hit:
                            b.active = False
                            var.boss_now.energy -= b.dmg
                            var.boss_now.hit = True
                            if var.boss_now.energy <=0:
                                var.score += var.boss_now.score
                                var.boss_now.active = False
                                
                #检测是否被击中
                for b in var.boss_bullet:
                    if b.active:
                        b.move()
                        screen.blit(b.image, b.rect)
                        boss_bullet_hit = pygame.sprite.collide_mask(b, var.me)
                        if boss_bullet_hit and not var.me.invincible:
                            b.active = False
                            var.me.active = False
                    
## --------------------------------游戏画面------------------------------------
            elif var.life_num and (not var.paused):
                #检测飞机碰撞
                enemies_down = pygame.sprite.spritecollide(var.me, var.enemies, False,pygame.sprite.collide_mask)
                if enemies_down and not var.me.invincible:
                    for each in enemies_down:
                        if each.active:
                            var.me.active = False
                            each.active = False
    
                #绘制敌机
                #大型敌机
                for each in var.big_enemies:
                    if each.active:
                        each.move()
                        if each.hit:
                            screen.blit(each.image_hit,each.rect)
                            each.hit = False
                        else:
                            if var.switch_image:
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
                        if not(var.delay % 3):
                            each.destroy_index = (each.destroy_index + 1) % 6
                            if each.destroy_index == 0:
                                var.score += each.__class__.score
                                enemy3_fly_sound.stop()
                                each.reset()
                    if each.rect.top == each.height:
                        enemy3_fly_sound.stop()
    
                #中型敌机
                for each in var.mid_enemies:
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
                        if not(var.delay % 3):
                            each.destroy_index = (each.destroy_index + 1) % 4
                            if each.destroy_index == 0:
                                var.score += each.__class__.score
                                each.reset()
    
                #小型敌机
                for each in var.small_enemies:
                    if each.active:
                        each.move()
                        screen.blit(each.image,each.rect)
                    else:
                        #毁灭
                        if not(var.delay % 3):
                            if each.destroy_index == 0:
                                enemy1_down_sound.play()
                            screen.blit(each.destroy_images[each.destroy_index],each.rect)
                            each.destroy_index = (each.destroy_index + 1) % 4
                            if each.destroy_index == 0:
                                var.score += each.__class__.score
                                each.reset()
    
                #检测是否击中敌机
                if var.bullets:
                    for b in var.bullets:
                        if b.active:
                            b.move()
                            screen.blit(b.image, b.rect)
                            enemy_hit = pygame.sprite.spritecollide(b, var.enemies, False, pygame.sprite.collide_mask)
                            if enemy_hit:
                                b.active = False
                                for e in enemy_hit:
                                    if e in var.mid_enemies or e in var.big_enemies:
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
