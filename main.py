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
import sql
import variables as var

class Game():
    def __init__(self):
        #初始化
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)
        self.bg_size = width, height = 480, 700
        self.screen = pygame.display.set_mode(self.bg_size)
        pygame.display.set_caption('飞机大战')
        icon = pygame.image.load('images/icon.gif').convert()
        pygame.display.set_icon(icon)
        self.background = pygame.image.load('images/background.png').convert()
        self.BLACK = (0,0,0)
        self.GREEN = (0,255,0)
        self.RED = (255,0,0)
        self.WHITE = (255,255,255)

        #载入音乐，音效
        pygame.mixer.music.set_volume(0.2)

        self.bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
        self.bullet_sound.set_volume(0.2)
        
        self.bomb_sound = pygame.mixer.Sound('sound/use_bomb.wav')
        self.bomb_sound.set_volume(0.2)
        
        self.supply_sound = pygame.mixer.Sound('sound/supply.wav')
        self.supply_sound.set_volume(0.2)
        
        self.get_bomb_sound = pygame.mixer.Sound('sound/get_bomb.wav')
        self.get_bomb_sound.set_volume(0.2)
        self.get_bullet_sound = pygame.mixer.Sound('sound/get_bullet.wav')
        self.get_bullet_sound.set_volume(0.2)
        
        self.upgrade_sound = pygame.mixer.Sound('sound/upgrade.wav')
        self.upgrade_sound.set_volume(0.2)
        
        self.enemy3_fly_sound = pygame.mixer.Sound('sound/enemy3_flying.wav')
        self.enemy3_fly_sound.set_volume(0.2)
        
        self.enemy1_down_sound = pygame.mixer.Sound('sound/enemy1_down.wav')
        self.enemy1_down_sound.set_volume(0.1)
        self.enemy2_down_sound = pygame.mixer.Sound('sound/enemy2_down.wav')
        self.enemy2_down_sound.set_volume(0.2)
        self.enemy3_down_sound = pygame.mixer.Sound('sound/enemy3_down.wav')
        self.enemy3_down_sound.set_volume(0.5)
        self.me_down_sound = pygame.mixer.Sound('sound/me_down.wav')
        self.me_down_sound.set_volume(0.2)

        #主程序
        init_thread = var.Initializer(self)
        init_thread.daemon = True
        init_thread.start()
        clock = pygame.time.Clock()
        running = True
        var.init(self)
    
        while running:
            for event in pygame.event.get():
                if event.type == gloc.QUIT:
                    pygame.quit()
                    sys.exit()
    
                #发放补给包
                elif event.type == self.SUPPLY_TIME:
                    self.supply_sound.play()
                    pygame.time.set_timer(self.SUPPLY_TIME, 30000)
                    self.supply_time = time.time()
                    if self.score > 750000:
                        if random.choice([True,False]):
                            if random.choice([True,False]):
                                self.bomb_supply.reset()
                            else:
                                self.bullet_supply.reset()
                        else:
                            if random.choice([True,False]):
                                self.medical_supply.reset()
                            else:
                                self.bullet_update.reset()
                    elif random.choice([True,False]):
                        self.bomb_supply.reset()
                    else:
                        self.bullet_supply.reset()
    
                #超级子弹计时器
                elif event.type == self.DOUBLE_BULLET_TIME:
                    self.is_double = False
                    self.bullet2 = var.init_bullet(
                        bullet.Bullet2,
                        self.BULLET2_NUM,
                        (self.me.rect.centerx-33, self.me.rect.centery),
                        (self.me.rect.centerx+30, self.me.rect.centery))
                    self.bullet4 = var.init_bullet(
                        bullet.Bullet4,
                        self.BULLET4_NUM,
                        (self.me.rect.centerx-33, self.me.rect.centery),
                        (self.me.rect.centerx+30, self.me.rect.centery))
                    pygame.time.set_timer(self.DOUBLE_BULLET_TIME, 0)
    
                #检测用户按键
                elif event.type == gloc.KEYDOWN:
                    #检测用户使用全屏炸弹
                    if event.key == gloc.K_SPACE:
                        if self.me.bomb_num and (not self.paused):
                            self.me.bomb_num -= 1
                            self.me.bomb_action = True
                            self.bomb_sound.play()
                            if self.boss_appear:
                                self.boss_now.energy -= 30
                                for each in self.boss_bullet:
                                    each.active = False
                            else:
                                var.kill_enemies(self.enemies)
                                        
                    #检测用户p键暂停
                    elif event.key == gloc.K_p or event.key == gloc.K_ESCAPE:
                        self.paused = not self.paused
                        if self.paused:
                            self.paused_image = self.resume_pressed_image
                            self.paused_time = time.time()
                            pygame.time.set_timer(self.SUPPLY_TIME, 0)
                            pygame.mixer.music.pause()
                            pygame.mixer.pause()
                        else:
                            self.paused_image = self.pause_pressed_image
                            if not self.start and not self._help:
                                pygame.time.set_timer(self.SUPPLY_TIME, 30000-round((self.paused_time-self.supply_time)*1000))
                            pygame.mixer.music.unpause()
                            pygame.mixer.unpause()
    
                #己方飞机无敌计时
                elif event.type == self.INVINCIBLE_TIME:
                    self.me.invincible = False
                    pygame.time.set_timer(self.INVINCIBLE_TIME, 0)
    
                #检测鼠标暂停操作
                elif event.type == gloc.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.paused_rect.collidepoint(event.pos):
                        self.paused = not self.paused
                        if self.paused:
                            self.paused_image = self.resume_pressed_image
                            self.paused_time = time.time()
                            pygame.time.set_timer(self.SUPPLY_TIME, 0)
                            pygame.mixer.music.pause()
                            pygame.mixer.pause()
                        else:
                            self.paused_image = self.pause_pressed_image
                            if not self.start and not self._help:
                                pygame.time.set_timer(self.SUPPLY_TIME, 30000-round((self.paused_time-self.supply_time)*1000))
                            pygame.mixer.music.unpause()
                            pygame.mixer.unpause()
                elif event.type == gloc.MOUSEMOTION:
                    if self.paused_rect.collidepoint(event.pos):
                        if self.paused:
                            self.paused_image = self.resume_pressed_image
                        else:
                            self.paused_image = self.pause_pressed_image
                    else:
                        if self.paused:
                            self.paused_image = self.resume_nor_image
                        else:
                            self.paused_image = self.pause_nor_image
    
            #根据用户得分增加难度
            if self.level == 1 and self.score > 50000:
                self.level = 2
                self.upgrade_sound.play()
                #增加3架小型飞机，2架中型飞机，1架大型飞机
                var.add_enemies(enemy.SmallEnemy, 3, self.small_enemies, self.enemies)
                var.add_enemies(enemy.MidEnemy, 2, self.mid_enemies, self.enemies)
                var.add_enemies(enemy.BigEnemy, 1, self.big_enemies, self.enemies)
                #提升速度
                var.inc_speed(self.small_enemies, 1)
    
            elif self.level == 2 and self.score > 300000:
                self.level = 3
                self.upgrade_sound.play()
                #增加5架小型飞机，3架中型飞机，2架大型飞机
                var.add_enemies(enemy.SmallEnemy, 5, self.small_enemies, self.enemies)
                var.add_enemies(enemy.MidEnemy, 3, self.mid_enemies, self.enemies)
                var.add_enemies(enemy.BigEnemy, 2, self.big_enemies, self.enemies)
                #提升速度
                var.inc_speed(self.small_enemies, 1)
                var.inc_speed(self.mid_enemies, 1)
    
            elif self.level == 3 and self.score > 600000:
                self.level = 4
                self.upgrade_sound.play()
                #增加5架小型飞机，3架中型飞机，2架大型飞机
                var.add_enemies(enemy.SmallEnemy, 5, self.small_enemies, self.enemies)
                var.add_enemies(enemy.MidEnemy, 3, self.mid_enemies, self.enemies)
                var.add_enemies(enemy.BigEnemy, 2, self.big_enemies, self.enemies)
                #提升速度
                var.inc_speed(self.small_enemies, 1)
                var.inc_speed(self.mid_enemies, 1)
    
            elif self.level == 4 and self.score > 1000000:
                self.level = 5
                self.upgrade_sound.play()
                #增加5架小型飞机，3架中型飞机，2架大型飞机
                var.add_enemies(enemy.SmallEnemy, 5, self.small_enemies, self.enemies)
                var.add_enemies(enemy.MidEnemy, 3, self.mid_enemies, self.enemies)
                var.add_enemies(enemy.BigEnemy, 2, self.big_enemies, self.enemies)
                #提升速度
                var.inc_speed(self.small_enemies, 1)
                var.inc_speed(self.mid_enemies, 1)
                
            #根据用户得分出现boss
            if self.boss_lv == 0 and self.score > 100000:
                self.boss_lv = 1
                self.boss_now = self.boss_lv1
                self.boss_bullet = self.boss_bullet_1
                self.boss_appear = True
                self.transition = True
                self.me.bomb_action = False
                var.kill_enemies(self.enemies)
                var.change_music(True)
            elif self.boss_lv == 1 and self.score > 350000:
                self.boss_lv = 2
                self.boss_now = self.boss_lv2
                self.boss_bullet = self.boss_bullet_2
                self.boss_appear = True
                self.transition = True
                self.me.bomb_action = False
                var.kill_enemies(self.enemies)
                var.change_music(True)
            elif self.boss_lv == 2 and self.score > 750000:
                self.boss_lv = 3
                self.boss_now = self.boss_lv3
                self.boss_bullet = self.boss_bullet_3
                self.boss_appear = True
                self.transition = True
                self.me.bomb_action = False
                var.kill_enemies(self.enemies)
                var.change_music(True)
    
            self.screen.blit(self.background,(0,0))
            
## --------------------------------游戏开始画面---------------------------------
            if self.start and not self._help:
                self.screen.blit(self.title_image, self.title_image_rect)
                self.screen.blit(self.start_image, self.start_rect)
                self.screen.blit(self.help_image, self.help_rect)
                self.screen.blit(self.exit_image, self.exit_rect)
                self.screen.blit(self.author_text, self.author_text_rect)
                
                record_score_text = self.score_font.render('Best : %d' % self.record_score, True, self.WHITE)
                self.screen.blit(record_score_text, (50,50))
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if self.start_rect.collidepoint(pos):
                        self.start = False
                        if self.paused:
                            self.paused = False
                            self.paused_image = self.pause_pressed_image
                            pygame.mixer.music.unpause()
                            pygame.mixer.unpause()
                        self.supply_time = time.time()
                        pygame.time.set_timer(self.SUPPLY_TIME, 30000)
                    elif self.help_rect.collidepoint(pos):
                        self._help = True
                    elif self.exit_rect.collidepoint(pos):
                        pygame.quit()
                        sys.exit()
                        
## --------------------------------帮助画面------------------------------------
            elif self._help:
                help_image1 = pygame.image.load('images/help/help1.png').convert_alpha()
                help_image2 = pygame.image.load('images/help/help2.png').convert_alpha()
                back_image1 = pygame.image.load('images/help/back1.png').convert_alpha()
                back_image2 = pygame.image.load('images/help/back2.png').convert_alpha()
                if self.switch_image:
                    self.screen.blit(help_image1, (10,0))
                    self.screen.blit(back_image1, (0,0))
                else:
                    self.screen.blit(help_image2, (10,0))
                    self.screen.blit(back_image2, (0,0))
                    
                #切换图片
                if not (self.delay % 5):
                    self.switch_image = not self.switch_image
                self.delay -= 1
                if not self.delay:
                    self.delay = 100
                    
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if back_image1.get_rect().collidepoint(pos):
                        self._help = False
            
## --------------------------------背景过渡------------------------------------
            elif self.transition:
                #毁灭画面中敌方飞机
                self.enemy3_fly_sound.stop()
                if self.trans_delay:
                    self.trans_delay -= 1
                    for each in self.enemies:
                        if each.rect.bottom > 0 and (not each.active):
                            self.screen.blit(each.destroy_images[each.destroy_index], each.rect)
                            if not(self.trans_delay % 3):
                                each.destroy_index = (each.destroy_index + 1) % 4
                                if each.destroy_index == 0:
                                    each.reset()
                    #绘制我方飞机
                    if self.me.active:
                        if self.switch_image:
                            self.screen.blit(self.me.image1, self.me.rect)
                        else:
                            self.screen.blit(self.me.image2, self.me.rect)
                    
                    #切换图片
                    if not (self.trans_delay % 5):
                        self.switch_image = not self.switch_image
                #背景过渡
                else:
                    if self.boss_appear:
                        self.trans_num += 1
                        self.screen.blit(self.boss_now.transitional_image[self.boss_now.transitional_index],(0,0))
                        if not (self.trans_num % 4):
                            self.boss_now.transitional_index = (self.boss_now.transitional_index + 1) % len(self.boss_now.transitional_image)
                            if not self.boss_now.transitional_index:
                                self.me.init_image()
                                self.trans_num = 0
                                self.transition = False
                    else:
                        self.trans_num += 1
                        self.screen.blit(self.boss_now.background, (0,0))
                        self.screen.blit(self.boss_now.destroy_image[self.boss_now.destroy_index],(0,0))
                        if not (self.trans_num % 6):
                            self.boss_now.destroy_index = (self.boss_now.destroy_index + 1) % len(self.boss_now.destroy_image)
                            if not self.boss_now.destroy_index:
                                self.me.init_image(True)
                                self.me.bomb_action = False
                                self.trans_num = 0
                                self.trans_delay = 12
                                var.change_music()
                                self.transition = False
            
## ------------------------------游戏结束画面-----------------------------------
            elif self.life_num == 0:
                pygame.mixer.music.stop()
                pygame.mixer.stop()
                pygame.time.set_timer(self.SUPPLY_TIME, 0)
                if not self.recorded:
                    self.recorded = True
                    if self.score > self.record_score:
                        sql.Sql.set_score(self.score)
                            
                record_score_text = self.score_font.render('Best : %d' % self.record_score, True, self.WHITE)
                self.screen.blit(record_score_text, (50,50))
                
                gameover_text1 = self.gameover_font.render('Your Score', True, self.WHITE)
                gameover_text1_rect = gameover_text1.get_rect()
                gameover_text1_rect.left, gameover_text1_rect.top = (width - gameover_text1_rect.width) // 2, height // 3
                self.screen.blit(gameover_text1, gameover_text1_rect)
                
                gameover_text2 = self.gameover_font.render(str(self.score), True, self.WHITE)
                gameover_text2_rect = gameover_text2.get_rect()
                gameover_text2_rect.left, gameover_text2_rect.top = (width - gameover_text2_rect.width) // 2, gameover_text1_rect.bottom + 10
                self.screen.blit(gameover_text2, gameover_text2_rect)
                
                self.again_rect.left, self.again_rect.top = (width - self.again_rect.width) // 2, gameover_text2_rect.bottom + 50
                self.screen.blit(self.again_image, self.again_rect)
                
                self.gameover_rect.left = (width - self.gameover_rect.width) // 2
                self.gameover_rect.top = self.again_rect.bottom + 10
                self.screen.blit(self.gameover_image, self.gameover_rect)
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if self.again_rect.collidepoint(pos):
                        init_thread = var.Initializer(self)
                        init_thread.daemon = True
                        init_thread.start()
                        var.init(self)
                    elif self.gameover_rect.collidepoint(pos):
                        pygame.quit()
                        sys.exit()
## ----------------------------------------------------------------------------
            else:
                #boss背景
                if self.boss_appear:
                    self.screen.blit(self.boss_now.background,(0,0))
                    
                #暂停界面
                if self.paused:
                    self.screen.blit(self.pause_restart, self.pause_restart_rect)
                    self.screen.blit(self.pause_quit, self.pause_quit_rect)
                    if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        if self.pause_restart_rect.collidepoint(pos):
                            init_thread = var.Initializer(self)
                            init_thread.daemon = True
                            init_thread.start()
                            var.init(self)
                        elif self.pause_quit_rect.collidepoint(pos):
                            self.life_num = 0
                    
                if not self.paused:
                    #检测键盘按键操作
                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[gloc.K_w] or key_pressed[gloc.K_UP]:
                        self.me.moveUp()
                    if key_pressed[gloc.K_s] or key_pressed[gloc.K_DOWN]:
                        self.me.moveDown()
                    if key_pressed[gloc.K_a] or key_pressed[gloc.K_LEFT]:
                        self.me.moveLeft()
                    if key_pressed[gloc.K_d] or key_pressed[gloc.K_RIGHT]:
                        self.me.moveRight()
                
                #绘制我方飞机
                if self.me.active:
                    if self.switch_image:
                        self.screen.blit(self.me.image1, self.me.rect)
                    else:
                        self.screen.blit(self.me.image2, self.me.rect)
                    if self.me.invincible:
                        self.screen.blit(
                                self.me.shield,
                                (self.me.rect.centerx - self.me.shield_rect.width // 2,
                                 self.me.rect.centery - self.me.shield_rect.height // 2))
                else:
                    #毁灭
                    if self.me.destroy_index == 0:
                        self.me_down_sound.play()
                    self.screen.blit(self.me.destroy_images[self.me.destroy_index],self.me.rect)
                    if not(self.delay % 3):
                        self.me.destroy_index = (self.me.destroy_index + 1) % 4
                        if self.me.destroy_index == 0:
                            self.life_num -= 1
                            self.me.reset()
                            self.update = False
                            pygame.time.set_timer(self.INVINCIBLE_TIME, 3000)
                            
                #全屏炸弹效果
                if self.me.bomb_action:
                    self.screen.blit(self.me.bomb_images[self.me.bomb_action_index], (0,0))
                    if not (self.delay % 6):
                        self.me.bomb_action_index = (self.me.bomb_action_index + 1) % 6
                        if not self.me.bomb_action_index:
                            self.me.bomb_action = False
                
                #绘制子弹
                if not (self.delay % 10) and (not self.paused):
                    self.bullet_sound.play()
                    if self.is_double:
                        if self.update:
                            self.bullets = self.bullet4
                            self.bullets[self.bullet4_index].reset((self.me.rect.centerx-33,self.me.rect.centery))
                            self.bullets[self.bullet4_index+1].reset((self.me.rect.centerx+30,self.me.rect.centery))
                            self.bullet4_index = (self.bullet4_index + 2) % self.BULLET4_NUM
                        else:
                            self.bullets = self.bullet2
                            self.bullets[self.bullet2_index].reset((self.me.rect.centerx-33,self.me.rect.centery))
                            self.bullets[self.bullet2_index+1].reset((self.me.rect.centerx+30,self.me.rect.centery))
                            self.bullet2_index = (self.bullet2_index + 2) % self.BULLET2_NUM
                    else:
                        if self.update:
                            self.bullets = self.bullet3
                            self.bullets[self.bullet3_index].reset(self.me.rect.midtop)
                            self.bullet3_index = (self.bullet3_index + 1) % self.BULLET3_NUM
                        else:
                            self.bullets = self.bullet1
                            self.bullets[self.bullet1_index].reset(self.me.rect.midtop)
                            self.bullet1_index = (self.bullet1_index + 1) % self.BULLET1_NUM
                
                #绘制炸弹
                bomb_text = self.me.bomb_font.render('× %d' % self.me.bomb_num, True, self.WHITE)
                self.screen.blit(self.me.bomb_image, (10, height - 10 - self.me.bomb_rect.height))
                self.screen.blit(bomb_text, (20 + self.me.bomb_rect.width, height - 10 - self.me.bomb_rect.height))
    
                #绘制剩余生命条数
                if self.life_num:
                    for i in range(self.life_num):
                        self.screen.blit(self.me.life_image, \
                                    (width-10-(i+1)*self.me.life_rect.width, \
                                     height-10-self.me.life_rect.height))
                #绘制得分
                score_text = self.score_font.render('Score : %s' % str(self.score), True, self.WHITE)
                self.screen.blit(score_text,(10,5))
                    
                #绘制全屏炸弹补给包
                if self.bomb_supply.active and not self.paused:
                    self.bomb_supply.move()
                    self.screen.blit(self.bomb_supply.image, self.bomb_supply.rect)
                    if pygame.sprite.collide_mask(self.bomb_supply, self.me):
                        self.get_bomb_sound.play()
                        if self.me.bomb_num < 3:
                            self.me.bomb_num += 1
                        self.bomb_supply.active = False
    
                #绘制超级子弹补给包
                if self.bullet_supply.active and not self.paused:
                    self.bullet_supply.move()
                    self.screen.blit(self.bullet_supply.image, self.bullet_supply.rect)
                    if pygame.sprite.collide_mask(self.bullet_supply, self.me):
                        self.get_bullet_sound.play()
                        self.is_double = True
                        self.bullet1 = var.init_bullet(bullet.Bullet1, self.BULLET1_NUM, self.me.rect.midtop)
                        self.bullet3 = var.init_bullet(bullet.Bullet3, self.BULLET3_NUM, self.me.rect.midtop)
                        pygame.time.set_timer(self.DOUBLE_BULLET_TIME, 18000)
                        self.bullet_supply.active = False
                        
                #绘制升级子弹补给包
                if self.bullet_update.active and not self.paused:
                    self.bullet_update.move()
                    self.screen.blit(self.bullet_update.image, self.bullet_update.rect)
                    if pygame.sprite.collide_mask(self.bullet_update, self.me):
                        self.get_bullet_sound.play()
                        self.update = True
                        self.bullet1 = var.init_bullet(bullet.Bullet1, self.BULLET1_NUM, self.me.rect.midtop)
                        self.bullet2 = var.init_bullet(
                            bullet.Bullet2,
                            self.BULLET2_NUM,
                            (self.me.rect.centerx-33, self.me.rect.centery),
                            (self.me.rect.centerx+30, self.me.rect.centery))
                        self.bullet_update.active = False
                
                #绘制医疗包
                if self.medical_supply.active and not self.paused:
                    self.medical_supply.move()
                    self.screen.blit(self.medical_supply.image, self.medical_supply.rect)
                    if pygame.sprite.collide_mask(self.medical_supply, self.me):
                        self.get_bomb_sound.play()
                        if self.life_num < 3:
                            self.life_num += 1
                        self.medical_supply.active = False
                        
                #跟随时间加分
                if not (self.delay % 60) and not self.paused:
                    self.score += 1000
    
                #切换图片
                if not (self.delay % 5) and not self.paused:
                    self.switch_image = not self.switch_image
                    
                self.delay -= 1
                if not self.delay:
                    self.delay = 100
                
## -------------------------------boss画面-------------------------------------
                if self.boss_appear and (not self.paused) and (not self.transition):
                    #检测飞机碰撞
                    boss_down = pygame.sprite.spritecollide(self.me, self.boss_group, False, pygame.sprite.collide_mask)
                    if boss_down and not self.me.invincible:
                        if self.boss_now.active:
                            self.me.active = False
                                
                    #绘制boss
                    if self.boss_now.active:
                        self.boss_now.move_in()
                        self.boss_now.move()
                        if self.boss_now.hit:
                            self.screen.blit(self.boss_now.image_hit, self.boss_now.rect)
                            self.boss_now.hit = False
                        else:
                            self.screen.blit(self.boss_now.image, self.boss_now.rect)
                            
                        #绘制血槽
                        pygame.draw.line(
                                self.screen,
                                self.BLACK,
                                (self.boss_now.rect.left, self.boss_now.rect.top - 5),
                                (self.boss_now.rect.right,self.boss_now.rect.top - 5),
                                4)
                        boss_now_remain = self.boss_now.energy / self.boss_now.__class__.energy
                        if boss_now_remain > 0.2:
                            self.boss_now.energy_color = self.GREEN
                        else:
                            self.boss_now.energy_color = self.RED
                        pygame.draw.line(
                                self.screen,
                                self.boss_now.energy_color,
                                (self.boss_now.rect.left, self.boss_now.rect.top - 5),
                                (self.boss_now.rect.left + self.boss_now.rect.width*boss_now_remain, self.boss_now.rect.top - 5),
                                4)
                    else:
                        for each in self.boss_bullet:
                            each.active = False
                        if random.choice([True, False]):
                            self.bullet_update.reset()
                        else:
                            self.medical_supply.reset()
                        self.boss_appear = False
                        self.transition = True
                        
                    #boss攻击
                    if (not self.delay % 70) and (self.boss_now.rect.top >= 53):
                        self.boss_bullet[self.boss_bullet_index].reset(
                                (self.boss_now.rect.centerx + random.randint(-100,40),
                                 self.boss_now.rect.centery)
                            )
                        self.boss_bullet_index = (self.boss_bullet_index + 1) % self.BOSS_BULLET_NUM
                        
                    
                    #检测是否击中敌机
                    for b in self.bullets:
                        if b.active:
                            b.move()
                            self.screen.blit(b.image, b.rect)
                            boss_hit = pygame.sprite.spritecollide(b, self.boss_group, False, pygame.sprite.collide_mask)
                            if boss_hit:
                                b.active = False
                                self.boss_now.energy -= b.dmg
                                self.boss_now.hit = True
                                if self.boss_now.energy <=0:
                                    self.score += self.boss_now.score
                                    self.boss_now.active = False
                                    
                    #检测是否被击中
                    for b in self.boss_bullet:
                        if b.active:
                            b.move()
                            self.screen.blit(b.image, b.rect)
                            boss_bullet_hit = pygame.sprite.collide_mask(b, self.me)
                            if boss_bullet_hit and not self.me.invincible:
                                b.active = False
                                self.me.active = False
                        
## --------------------------------游戏画面------------------------------------
                elif self.life_num and (not self.paused):
                    #检测飞机碰撞
                    enemies_down = pygame.sprite.spritecollide(self.me, self.enemies, False,pygame.sprite.collide_mask)
                    if enemies_down and not self.me.invincible:
                        for each in enemies_down:
                            if each.active:
                                self.me.active = False
                                each.active = False
        
                    #绘制敌机
                    #大型敌机
                    for each in self.big_enemies:
                        if each.active:
                            each.move()
                            if each.hit:
                                self.screen.blit(each.image_hit,each.rect)
                                each.hit = False
                            else:
                                if self.switch_image:
                                    self.screen.blit(each.image1,each.rect)
                                else:
                                    self.screen.blit(each.image2,each.rect)
                            #绘制血槽
                            pygame.draw.line(
                                    self.screen,
                                    self.BLACK,
                                    (each.rect.left,each.rect.top - 5),
                                    (each.rect.right,each.rect.top - 5),
                                    2)
                            big_energy_remain = each.energy / each.__class__.energy
                            if big_energy_remain > 0.2:
                                each.energy_color = self.GREEN
                            else:
                                each.energy_color = self.RED
                            pygame.draw.line(
                                    self.screen,
                                    each.energy_color,
                                    (each.rect.left,each.rect.top - 5),
                                    (each.rect.left + each.rect.width*big_energy_remain,each.rect.top - 5),
                                    2)
                            
                            #大型提示音效
                            if each.rect.bottom == -50:
                                self.enemy3_fly_sound.play(-1)
                        else:
                            #毁灭
                            if each.destroy_index == 0:
                                self.enemy3_down_sound.play()
                            self.screen.blit(each.destroy_images[each.destroy_index],each.rect)
                            if not(self.delay % 3):
                                each.destroy_index = (each.destroy_index + 1) % 6
                                if each.destroy_index == 0:
                                    self.score += each.__class__.score
                                    self.enemy3_fly_sound.stop()
                                    each.reset()
                        if each.rect.top == each.height:
                            self.enemy3_fly_sound.stop()
        
                    #中型敌机
                    for each in self.mid_enemies:
                        if each.active:
                            each.move()
                            if each.hit:
                                self.screen.blit(each.image_hit,each.rect)
                                each.hit = False
                            else:
                                self.screen.blit(each.image,each.rect)
                            #绘制血槽
                            pygame.draw.line(
                                    self.screen,
                                    self.BLACK,
                                    (each.rect.left,each.rect.top - 5),
                                    (each.rect.right,each.rect.top - 5),
                                    2)
                            mid_energy_remain = each.energy / enemy.MidEnemy.energy
                            if mid_energy_remain > 0.2:
                                each.energy_color = self.GREEN
                            else:
                                each.energy_color = self.RED
                            pygame.draw.line(
                                    self.screen,
                                    each.energy_color,
                                    (each.rect.left,each.rect.top - 5),
                                    (each.rect.left + each.rect.width * mid_energy_remain,each.rect.top - 5),
                                    2)
                        else:
                            #毁灭
                            if each.destroy_index == 0:
                                self.enemy2_down_sound.play()
                            self.screen.blit(each.destroy_images[each.destroy_index],each.rect)
                            if not(self.delay % 3):
                                each.destroy_index = (each.destroy_index + 1) % 4
                                if each.destroy_index == 0:
                                    self.score += each.__class__.score
                                    each.reset()
        
                    #小型敌机
                    for each in self.small_enemies:
                        if each.active:
                            each.move()
                            self.screen.blit(each.image,each.rect)
                        else:
                            #毁灭
                            if not(self.delay % 3):
                                if each.destroy_index == 0:
                                    self.enemy1_down_sound.play()
                                self.screen.blit(each.destroy_images[each.destroy_index],each.rect)
                                each.destroy_index = (each.destroy_index + 1) % 4
                                if each.destroy_index == 0:
                                    self.score += each.__class__.score
                                    each.reset()
        
                    #检测是否击中敌机
                    if self.bullets:
                        for b in self.bullets:
                            if b.active:
                                b.move()
                                self.screen.blit(b.image, b.rect)
                                enemy_hit = pygame.sprite.spritecollide(b, self.enemies, False, pygame.sprite.collide_mask)
                                if enemy_hit:
                                    b.active = False
                                    for e in enemy_hit:
                                        if e in self.mid_enemies or e in self.big_enemies:
                                            e.hit = True
                                            e.energy -= b.dmg
                                            if e.energy <= 0:
                                                e.active = False
                                        else:
                                            e.active = False
    
            #绘制暂停按钮
            self.screen.blit(self.paused_image,self.paused_rect)
    
            pygame.display.flip()
            clock.tick(60)

if __name__ == '__main__':
    try:
        game = Game()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
