# -*- coding:utf-8 -*-
"""
These are the bullet objects of the game.
Author: yanyongyu
"""

__author__ = "yanyongyu"
__all__ = ['Bullet1', 'Bullet2', 'Bullet3', 'Bullet4',
           'Boss_bullet_lv1', 'Boss_bullet_lv2', 'Boss_bullet_lv3']

import pygame


class Bullet1(pygame.sprite.Sprite):
    def __init__(self, position, *args, **kw):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/bullet/bullet1.png')\
            .convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position

        self.active = False
        self.speed = 12
        self.dmg = 1

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < self.speed:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True


class Bullet2(pygame.sprite.Sprite):
    def __init__(self, position, *args, **kw):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/bullet/bullet2.png')\
            .convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position

        self.active = False
        self.speed = 14
        self.dmg = 1

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < self.speed:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True


class Bullet3(pygame.sprite.Sprite):
    def __init__(self, position, *args, **kw):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/bullet/bullet3.png')\
            .convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position

        self.active = False
        self.speed = 12
        self.dmg = 2

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < self.speed:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True


class Bullet4(pygame.sprite.Sprite):
    def __init__(self, position, *args, **kw):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/bullet/bullet4.png')\
            .convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 14
        self.active = False
        self.dmg = 2

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < self.speed:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True


class Boss_bullet_lv1(pygame.sprite.Sprite):
    def __init__(self, position, bg_size, *args, **kw):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('boss/lv1/boss_b1.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.rect.left, self.rect.top = position
        self.speed = 3
        self.active = False

    def move(self):
        self.rect.top += self.speed
        if self.rect.top > self.height:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True


class Boss_bullet_lv2(pygame.sprite.Sprite):
    def __init__(self, position, bg_size, *args, **kw):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('boss/lv2/boss_b2.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.rect.left, self.rect.top = position
        self.speed = 4
        self.active = False

    def move(self):
        self.rect.top += self.speed
        if self.rect.top > self.height:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True


class Boss_bullet_lv3(pygame.sprite.Sprite):
    def __init__(self, position, bg_size, *args, **kw):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('boss/lv3/boss_b3.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.rect.left, self.rect.top = position
        self.speed = 5
        self.active = False

    def move(self):
        self.rect.top += self.speed
        if self.rect.top > self.height:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True
