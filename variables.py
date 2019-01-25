# -*- coding: utf-8 -*-
"""
This is game variables.
Author: yanyongyu
"""

__author__ = "yanyongyu"

import time
import random
import threading

import pygame
import pygame.locals as gloc

import myplane
import enemy
import boss
import bullet
import supply
import sql

bg_size = width, height = 480, 700

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
    bullets = []
    for i in range(num // len(args)):
        for each in args:
            bullets.append(fn(each, bg_size))
    return bullets

#选择音乐，可选播放
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
        
#提升速度
def inc_speed(target: pygame.sprite.Group, inc: int) -> None:
    for each in target:
        each.speed += inc
        
#消灭屏幕中敌方飞机
def kill_enemies(group: pygame.sprite.Group) -> None:
    for each in group:
        if each.rect.bottom > 0:
            each.active = False

def init(game):
    #生成我方飞机
    game.me = myplane.MyPlane(bg_size)
    change_music()
    
    #生成子弹
    game.bullets = None
    game.update = False
    
    #等级选项
    game.level = 1
    
    #发放补给包
    game.supply_time = time.time()
    game.SUPPLY_TIME = gloc.USEREVENT
    
    #超级子弹定时器
    game.is_double = False
    
    #统计得分
    game.score = 0
    game.record_score = sql.Sql.get_score()
    
    #读取写入得分选项
    game.recorded = False
    
    #暂停选项
    game.paused = False
    if not hasattr(game, "pause_nor_image"):
        game.pause_nor_image = pygame.image.load('images/pause_nor.png').convert_alpha()
        game.pause_pressed_image = pygame.image.load('images/pause_pressed.png').convert_alpha()
        game.resume_nor_image = pygame.image.load('images/resume_nor.png').convert_alpha()
        game.resume_pressed_image = pygame.image.load('images/resume_pressed.png').convert_alpha()
        game.paused_rect = game.pause_nor_image.get_rect()
        game.paused_rect.left, game.paused_rect.top = width - game.paused_rect.width - 10, 10
    game.paused_image = game.pause_nor_image
    
    #切换图片
    game.switch_image = True
    
    #延迟切换
    game.delay = 100
    
    #生命条数
    game.life_num = 3
    
    #游戏开始画面
    game.start = True
    
    #帮助画面
    game._help = False
    
    #过渡画面
    game.transition = False
    game.trans_delay = 12
    game.trans_num = 0
    
    #Boss画面
    game.boss_lv = 0
    game.boss_appear = False
    
    #发放补给包
    if not hasattr(game, "bullet_supply"):
        game.bullet_supply = supply.Bullet_Supply(game.bg_size)
        game.bomb_supply = supply.Bomb_Supply(game.bg_size)
        game.bullet_update = supply.Bullet_Update(game.bg_size)
        game.medical_supply = supply.Medical_supply(game.bg_size)
        game.SUPPLY_TIME = gloc.USEREVENT
    pygame.time.set_timer(game.SUPPLY_TIME, 0)
    
    #超级子弹定时器
    if not hasattr(game, "DOUBLE_BULLET_TIME"):
        game.DOUBLE_BULLET_TIME = gloc.USEREVENT + 1
    pygame.time.set_timer(game.DOUBLE_BULLET_TIME, 0)
    
    #统计得分
    game.score_font = pygame.font.Font('font/font.ttf',36)
    
    #暂停选项
    if not hasattr(game, "pause_nor_iamge"):
        game.pause_nor_image = pygame.image.load('images/pause_nor.png').convert_alpha()
        game.pause_pressed_image = pygame.image.load('images/pause_pressed.png').convert_alpha()
        game.resume_nor_image = pygame.image.load('images/resume_nor.png').convert_alpha()
        game.resume_pressed_image = pygame.image.load('images/resume_pressed.png').convert_alpha()
        game.paused_rect = game.pause_nor_image.get_rect()
        game.paused_rect.left, game.paused_rect.top = width - game.paused_rect.width - 10, 10
        game.pause_restart = pygame.image.load('images/restart.png').convert_alpha()
        game.pause_restart_rect = game.pause_restart.get_rect()
        game.pause_restart_rect.left, game.pause_restart_rect.top = 130, 300
        game.pause_quit = pygame.image.load('images/quit.png').convert_alpha()
        game.pause_quit_rect = game.pause_quit.get_rect()
        game.pause_quit_rect.left, game.pause_quit_rect.top = 310, 300
    game.paused_image = game.pause_nor_image
    
    #无敌计时器
    if not hasattr(game, "INVINCIBLE_TIME"):
        game.INVINCIBLE_TIME = gloc.USEREVENT + 2
    pygame.time.set_timer(game.INVINCIBLE_TIME, 0)
    
    #游戏开始画面
    if not hasattr(game, "author_font"):
        game.title_image = pygame.image.load('images/start/title.png').convert_alpha()
        game.title_image_rect = game.title_image.get_rect()
        game.title_image_rect.left = (width - game.title_image_rect.width) // 2
        game.title_image_rect.top = (height // 3) - 40
        
        game.start_image = pygame.image.load('images/start/start.png').convert_alpha()
        game.start_rect = game.start_image.get_rect()
        game.start_rect.left = (width - game.start_rect.width) // 2
        game.start_rect.top = 413
        
        game.help_image = pygame.image.load('images/start/help.png').convert_alpha()
        game.help_rect = game.help_image.get_rect()
        game.help_rect.left = (width - game.help_rect.width) // 2
        game.help_rect.top = 463
        
        game.exit_image = pygame.image.load('images/start/exit.png').convert_alpha()
        game.exit_rect = game.exit_image.get_rect()
        game.exit_rect.left = (width - game.exit_rect.width) // 2
        game.exit_rect.top = 513
        
        game.author_font = pygame.font.Font('font/msyh.ttf',20)
        game.author_text = game.author_font.render('directed by : ShowTime--Joker', True, game.WHITE)
        game.author_text_rect = game.author_text.get_rect()
        game.author_text_rect.left = width - game.author_text_rect.width - 10
        game.author_text_rect.top = height - game.author_text_rect.height - 10
        
    #游戏结束画面
    if not hasattr(game, "gameover_font"):
        game.gameover_font = pygame.font.Font('font/font.ttf',48)
        game.again_image = pygame.image.load('images/start/again.png').convert_alpha()
        game.again_rect = game.again_image.get_rect()
        game.gameover_image = pygame.image.load('images/start/gameover.png').convert_alpha()
        game.gameover_rect = game.gameover_image.get_rect()
    
class Initializer(threading.Thread):
    def __init__(self, game):
        threading.Thread.__init__(self)
        self.game = game
        
    def run(self):
        #生成敌方飞机
        self.game.enemies = pygame.sprite.Group()
        #小型飞机
        self.game.small_enemies = pygame.sprite.Group()
        add_enemies(enemy.SmallEnemy, 15, self.game.small_enemies, self.game.enemies)
        #中型飞机
        self.game.mid_enemies = pygame.sprite.Group()
        add_enemies(enemy.MidEnemy, 4, self.game.mid_enemies, self.game.enemies)
        #大型飞机
        self.game.big_enemies = pygame.sprite.Group()
        add_enemies(enemy.BigEnemy, 2, self.game.big_enemies, self.game.enemies)
        
        #生成普通子弹
        self.game.bullet1_index = 0
        self.game.BULLET1_NUM = 4
        self.game.bullet1 = init_bullet(bullet.Bullet1, self.game.BULLET1_NUM, (240,1000))
        
        #生成超级子弹
        self.game.bullet2_index = 0
        self.game.BULLET2_NUM = 8
        self.game.bullet2 = init_bullet(
                bullet.Bullet2,
                self.game.BULLET2_NUM,
                (240,1000))
            
        #生成升级子弹
        self.game.bullet3_index = 0
        self.game.BULLET3_NUM = 4
        self.game.bullet3 = init_bullet(bullet.Bullet3, self.game.BULLET3_NUM, (240,1000))
            
        #生成超级升级子弹
        self.game.bullet4_index = 0
        self.game.BULLET4_NUM = 8
        self.game.bullet4 = init_bullet(
                bullet.Bullet4,
                self.game.BULLET4_NUM,
                (240,1000))
        
        #生成boss
        self.game.boss_now = None
        self.game.boss_group = pygame.sprite.Group()
        self.game.boss_lv1 = boss.Boss_lv1(bg_size)
        self.game.boss_lv2 = boss.Boss_lv2(bg_size)
        self.game.boss_lv3 = boss.Boss_lv3(bg_size)
        self.game.boss_group.add(self.game.boss_lv1, self.game.boss_lv2, self.game.boss_lv3)
        
        #生成boss子弹
        self.game.boss_bullet = None
        self.game.boss_bullet_index = 0
        self.game.BOSS_BULLET_NUM = 4
        #生成boss子弹1
        self.game.boss_bullet_1 = init_bullet(
                bullet.Boss_bullet_lv1,
                self.game.BOSS_BULLET_NUM,
                self.game.boss_lv1.rect.midbottom)
        #生成boss子弹2
        self.game.boss_bullet_2 = init_bullet(
                bullet.Boss_bullet_lv2,
                self.game.BOSS_BULLET_NUM,
                self.game.boss_lv2.rect.midbottom)
        #生成boss子弹3
        self.game.boss_bullet_3 = init_bullet(
                bullet.Boss_bullet_lv3,
                self.game.BOSS_BULLET_NUM,
                self.game.boss_lv3.rect.midbottom)
