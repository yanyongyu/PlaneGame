# -*- coding:utf-8 -*-
"""
These are the supply objects of the game.
Author: yanyongyu
"""

__author__ = "yanyongyu"
__all__ = ["Bullet_Supply", "Bomb_Supply"]

import pygame
import random

class Bullet_Supply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/supply/bullet_supply.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.rect.left = random.randint(0,self.width - self.rect.width)
        self.rect.bottom = -100
        
        self.speed = 5
        self.active = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left = random.randint(0,self.width - self.rect.width)
        self.rect.bottom = -100


class Bomb_Supply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/supply/bomb_supply.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.rect.left = random.randint(0, self.width - self.rect.width)
        self.rect.bottom = -100
        
        self.speed = 5
        self.active = False

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left = random.randint(0,self.width - self.rect.width)
        self.rect.bottom = -100
        
class Bullet_Update(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('images/supply/bullet_update.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.rect.left = random.randint(0, self.width - self.rect.width)
        self.rect.bottom = -100
        
        self.speed = 5
        self.active = False
        
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False
            
    def reset(self):
        self.active = True
        self.rect.left = random.randint(0, self.width - self.rect.width)
        self.rect.bottom = -100
        
class Medical_supply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('images/supply/medical_supply.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.rect.left = random.randint(0, self.width - self.rect.width)
        self.rect.bottom = -100
        
        self.speed = 5
        self.active = False
        
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False
            
    def reset(self):
        self.active = True
        self.rect.left = random.randint(0, self.width - self.rect.width)
        self.rect.bottom = -100
