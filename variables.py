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

def init():
    global me, bullets, update, level, supply_time, SUPPLY_TIME, is_double,\
        DOUBLE_BULLET_TIME, score, record_score, score_font, recorded, paused,\
        pause_nor_image, pause_pressed_image,\
        resume_nor_image, resume_pressed_image, paused_image, paused_rect,\
        switch_image, delay, life_num, start, _help, transition, trans_delay,\
        trans_num, boss_lv, boss_appear, author_font, start_image, start_rect,\
        help_image, help_rect, exit_image, exit_rect
    
    #生成我方飞机
    me = myplane.MyPlane(bg_size)
    change_music()
    
    #生成子弹
    bullets = None
    update = False
    
    #等级选项
    level = 1
    
    #发放补给包
    supply_time = time.time()
    SUPPLY_TIME = gloc.USEREVENT
    
    #超级子弹定时器
    is_double = False
    
    #统计得分
    score = 0
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
    
    #游戏开始画面
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
    
class Initializer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        global enemies, small_enemies, mid_enemies, big_enemies,\
            boss_now, boss_group, boss_lv1, boss_lv2, boss_lv3,\
            bullet1_index, bullet1, BULLET1_NUM,\
            bullet2_index, bullet2, BULLET2_NUM, bullet3_index,\
            bullet3, BULLET3_NUM, bullet4_index, bullet4, BULLET4_NUM, boss_bullet,\
            boss_bullet_index, BOSS_BULLET_NUM, boss_bullet_1, boss_bullet_2, boss_bullet_3
            
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
        
        #生成boss
        boss_now = None
        boss_group = pygame.sprite.Group()
        boss_lv1 = boss.Boss_lv1(bg_size)
        boss_lv2 = boss.Boss_lv2(bg_size)
        boss_lv3 = boss.Boss_lv3(bg_size)
        boss_group.add(boss_lv1, boss_lv2, boss_lv3)
        
        #生成boss子弹
        boss_bullet = None
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
