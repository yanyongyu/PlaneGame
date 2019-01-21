# -*- coding: utf-8 -*-
"""
These are the boss objects of the game.
Author: yanyongyu
"""

__author__ = 'yanyongyu'
__all__ = ['Boss_lv1', 'Boss_lv2', 'Boss_lv3']

import pygame
import random

class Boss_lv1(pygame.sprite.Sprite):
    energy = 100
    score = 10000
    
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('boss/lv1/lv1.png').convert_alpha()
        self.image_hit =  pygame.image.load('boss/lv1/lv1_hit.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.background = pygame.image.load('boss/bgimages/bg1.jpg').convert()
        
        self.transitional_index = 0
        self.transitional_image = [
                pygame.image.load('boss/lv1/1.png').convert_alpha(),
                pygame.image.load('boss/lv1/2.png').convert_alpha(),
                pygame.image.load('boss/lv1/3.png').convert_alpha(),
                pygame.image.load('boss/lv1/4.png').convert_alpha(),
                pygame.image.load('boss/lv1/5.png').convert_alpha(),
                pygame.image.load('boss/lv1/6.png').convert_alpha(),
                pygame.image.load('boss/lv1/7.png').convert_alpha(),
                pygame.image.load('boss/lv1/8.png').convert_alpha(),
                pygame.image.load('boss/lv1/9.png').convert_alpha(),
                pygame.image.load('boss/lv1/10.png').convert_alpha(),
                pygame.image.load('boss/lv1/11.png').convert_alpha(),
                pygame.image.load('boss/lv1/12.png').convert_alpha(),
                pygame.image.load('boss/lv1/13.png').convert_alpha(),
                pygame.image.load('boss/lv1/14.png').convert_alpha(),
                pygame.image.load('boss/lv1/15.png').convert_alpha(),
                pygame.image.load('boss/lv1/16.png').convert_alpha(),
                pygame.image.load('boss/lv1/17.png').convert_alpha(),
                pygame.image.load('boss/lv1/18.png').convert_alpha(),
                pygame.image.load('boss/lv1/19.png').convert_alpha(),
                pygame.image.load('boss/lv1/20.png').convert_alpha(),
                pygame.image.load('boss/lv1/21.png').convert_alpha(),
                pygame.image.load('boss/lv1/22.png').convert_alpha(),
                pygame.image.load('boss/lv1/23.png').convert_alpha(),
                pygame.image.load('boss/lv1/23_1.png').convert_alpha(),
                pygame.image.load('boss/lv1/23_2.png').convert_alpha(),
                pygame.image.load('boss/lv1/23_3.png').convert_alpha(),
                pygame.image.load('boss/lv1/24.png').convert_alpha(),
                pygame.image.load('boss/lv1/25.png').convert_alpha(),
                pygame.image.load('boss/lv1/26.png').convert_alpha(),
                pygame.image.load('boss/lv1/27.png').convert_alpha(),
                pygame.image.load('boss/lv1/28.png').convert_alpha(),
                pygame.image.load('boss/lv1/29.png').convert_alpha(),
                pygame.image.load('boss/lv1/30.png').convert_alpha(),
                pygame.image.load('boss/lv1/31.png').convert_alpha(),
                pygame.image.load('boss/lv1/32.png').convert_alpha(),
                pygame.image.load('boss/lv1/33.png').convert_alpha(),
            ]
        
        self.destroy_index = 0
        self.destroy_image = [
                pygame.image.load('boss/lv1/end_1.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_2.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_3.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_4.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_5.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_6.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_7.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_8.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_9.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_10.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_11.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_12.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_13.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_14.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_15.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_16.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_17.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_18.png').convert_alpha(),
                pygame.image.load('boss/lv1/end_19.png').convert_alpha()
            ]
        
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.rect.left = (self.width - self.rect.width) // 2
        self.rect.top = -0.2*self.height
        
        self.active = True
        self.energy = Boss_lv1.energy
        self.energy_color = None
        self.hit = False
        
        self.move_in_speed = 1
        self.move_speed = random.randint(1,3)
        self.move_direction = random.choice([-1,1])
        
    def move_in(self):
        if self.rect.top < 53:
            self.rect.top += self.move_in_speed
    
    def move(self):
        if self.rect.top >= 53:
            if self.rect.left <= 0:
                self.move_direction = 1
                self.move_speed = random.randint(1,3)
            elif self.rect.left >= self.width - self.rect.width:
                self.move_direction = -1
                self.move_speed = random.randint(1,3)
            self.rect.left += self.move_direction * self.move_speed
            
class Boss_lv2(pygame.sprite.Sprite):
    energy = 200
    score = 20000
    
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('boss/lv2/lv2.png').convert_alpha()
        self.image_hit =  pygame.image.load('boss/lv2/lv2_hit.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.background = pygame.image.load('boss/bgimages/bg2.jpg').convert()
        
        self.transitional_index = 0
        self.transitional_image = [
                pygame.image.load('boss/lv2/1.png').convert_alpha(),
                pygame.image.load('boss/lv2/2.png').convert_alpha(),
                pygame.image.load('boss/lv2/4.png').convert_alpha(),
                pygame.image.load('boss/lv2/5.png').convert_alpha(),
                pygame.image.load('boss/lv2/6.png').convert_alpha(),
                pygame.image.load('boss/lv2/8.png').convert_alpha(),
                pygame.image.load('boss/lv2/9.png').convert_alpha(),
                pygame.image.load('boss/lv2/10.png').convert_alpha(),
                pygame.image.load('boss/lv2/11.png').convert_alpha(),
                pygame.image.load('boss/lv2/12.png').convert_alpha(),
                pygame.image.load('boss/lv2/13.png').convert_alpha(),
                pygame.image.load('boss/lv2/14.png').convert_alpha(),
                pygame.image.load('boss/lv2/15.png').convert_alpha(),
                pygame.image.load('boss/lv2/16.png').convert_alpha(),
                pygame.image.load('boss/lv2/17.png').convert_alpha(),
                pygame.image.load('boss/lv2/18.png').convert_alpha(),
                pygame.image.load('boss/lv2/19.png').convert_alpha(),
                pygame.image.load('boss/lv2/20.png').convert_alpha(),
                pygame.image.load('boss/lv2/21.png').convert_alpha(),
                pygame.image.load('boss/lv2/22.png').convert_alpha(),
                pygame.image.load('boss/lv2/23.png').convert_alpha(),
                pygame.image.load('boss/lv2/24.png').convert_alpha(),
                pygame.image.load('boss/lv2/24_1.png').convert_alpha(),
                pygame.image.load('boss/lv2/24_2.png').convert_alpha(),
                pygame.image.load('boss/lv2/24_3.png').convert_alpha(),
                pygame.image.load('boss/lv2/25.png').convert_alpha(),
                pygame.image.load('boss/lv2/26.png').convert_alpha(),
                pygame.image.load('boss/lv2/27.png').convert_alpha(),
                pygame.image.load('boss/lv2/28.png').convert_alpha(),
                pygame.image.load('boss/lv2/29.png').convert_alpha(),
                pygame.image.load('boss/lv2/30.png').convert_alpha(),
                pygame.image.load('boss/lv2/31.png').convert_alpha(),
                pygame.image.load('boss/lv2/32.png').convert_alpha(),
            ]
        
        self.destroy_index = 0
        self.destroy_image = [
                pygame.image.load('boss/lv2/end_1.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_2.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_3.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_4.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_5.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_6.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_7.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_8.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_9.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_10.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_11.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_12.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_13.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_14.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_15.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_16.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_17.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_18.png').convert_alpha(),
                pygame.image.load('boss/lv2/end_19.png').convert_alpha()
            ]
        
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.rect.left = (self.width - self.rect.width) // 2
        self.rect.top = -0.2*self.height
        
        self.active = True
        self.energy = Boss_lv2.energy
        self.energy_color = None
        self.hit = False
        
        self.move_in_speed = 1
        self.move_delay = 50
        self.move_speed = random.randint(1,5)
        self.move_direction = random.choice([-1,1])
        
    def move_in(self):
        if self.rect.top < 53:
            self.rect.top += self.move_in_speed
            
    def move(self):
        if self.rect.top >= 53:
            if self.rect.left <= 0:
                self.move_direction = 1
                self.move_speed = random.randint(1,5)
            elif self.rect.left >= self.width - self.rect.width:
                self.move_direction = -1
                self.move_speed = random.randint(1,5)
            self.rect.left += self.move_direction * self.move_speed
            
            self.move_delay -= 1
            if not self.move_delay:
                self.move_delay = 50
                self.rect.top += 1
            
            
class Boss_lv3(pygame.sprite.Sprite):
    energy = 300
    score = 30000
    
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('boss/lv3/lv3.png').convert_alpha()
        self.image_hit =  pygame.image.load('boss/lv3/lv3_hit.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.background = pygame.image.load('boss/bgimages/bg3.jpg').convert()
        
        self.transitional_index = 0
        self.transitional_image = [
                pygame.image.load('boss/lv3/1.png').convert_alpha(),
                pygame.image.load('boss/lv3/2.png').convert_alpha(),
                pygame.image.load('boss/lv3/4.png').convert_alpha(),
                pygame.image.load('boss/lv3/5.png').convert_alpha(),
                pygame.image.load('boss/lv3/6.png').convert_alpha(),
                pygame.image.load('boss/lv3/8.png').convert_alpha(),
                pygame.image.load('boss/lv3/9.png').convert_alpha(),
                pygame.image.load('boss/lv3/10.png').convert_alpha(),
                pygame.image.load('boss/lv3/11.png').convert_alpha(),
                pygame.image.load('boss/lv3/12.png').convert_alpha(),
                pygame.image.load('boss/lv3/13.png').convert_alpha(),
                pygame.image.load('boss/lv3/14.png').convert_alpha(),
                pygame.image.load('boss/lv3/15.png').convert_alpha(),
                pygame.image.load('boss/lv3/16.png').convert_alpha(),
                pygame.image.load('boss/lv3/17.png').convert_alpha(),
                pygame.image.load('boss/lv3/18.png').convert_alpha(),
                pygame.image.load('boss/lv3/19.png').convert_alpha(),
                pygame.image.load('boss/lv3/20.png').convert_alpha(),
                pygame.image.load('boss/lv3/20_1.png').convert_alpha(),
                pygame.image.load('boss/lv3/20_2.png').convert_alpha(),
                pygame.image.load('boss/lv3/20_3.png').convert_alpha(),
                pygame.image.load('boss/lv3/21.png').convert_alpha(),
                pygame.image.load('boss/lv3/22.png').convert_alpha(),
                pygame.image.load('boss/lv3/23.png').convert_alpha(),
                pygame.image.load('boss/lv3/24.png').convert_alpha(),
                pygame.image.load('boss/lv3/25.png').convert_alpha(),
                pygame.image.load('boss/lv3/26.png').convert_alpha(),
                pygame.image.load('boss/lv3/27.png').convert_alpha(),
                pygame.image.load('boss/lv3/28.png').convert_alpha()
            ]
        
        self.destroy_index = 0
        self.destroy_image = [
                pygame.image.load('boss/lv3/end_1.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_2.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_3.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_4.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_5.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_6.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_7.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_8.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_9.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_10.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_11.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_12.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_13.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_14.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_15.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_16.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_17.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_18.png').convert_alpha(),
                pygame.image.load('boss/lv3/end_19.png').convert_alpha()
            ]
        
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.rect.left = (self.width - self.rect.width) // 2
        self.rect.top = -0.2*self.height
        
        self.active = True
        self.energy = Boss_lv3.energy
        self.energy_color = None
        self.hit = False
        
        self.move_in_speed = 1
        self.move_delay = 20
        self.move_speed = random.randint(1,5)
        self.move_direction = random.choice([-1,1])
        
    def move_in(self):
        if self.rect.top < 53:
            self.rect.top += self.move_in_speed
            
    def move(self):
        if self.rect.top >= 53:
            if self.rect.left <= 0:
                self.move_direction = 1
                self.move_speed = random.randint(1,5)
            elif self.rect.left >= self.width - self.rect.width:
                self.move_direction = -1
                self.move_speed = random.randint(1,5)
            self.rect.left += self.move_direction * self.move_speed
            
            self.move_delay -= 1
            if not self.move_delay:
                self.move_delay = 20
                self.rect.top += 1