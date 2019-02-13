# -*- coding:utf-8 -*-
"""
This is the myplane object of the game.
Author: yanyongyu
"""

__author__ = "yanyongyu"
__all__ = ['MyPlane']

import pygame


class MyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.init_image(True)

        self.destroy_index = 0
        self.bomb_num = 3
        self.bomb_action = False
        self.bomb_action_index = 0

        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size
        self.rect.left = (self.width - self.rect.width)//2
        self.rect.top = self.height - self.rect.height - 60

        self.speed = 10
        self.active = True
        self.invincible = False

    def moveUp(self):
        if self.rect.top >= 10:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.bottom <= self.height - 70:
            self.rect.top += self.speed
        else:
            self.rect.top = self.height - self.rect.height - 60

    def moveLeft(self):
        if self.rect.left >= 10:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right <= self.width - 10:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width

    def reset(self):
        self.rect.left = (self.width - self.rect.width)//2
        self.rect.top = self.height - self.rect.height - 60
        self.active = True
        self.invincible = True

    def init_image(self, reverse=False):
        if not reverse:
            self.image1 = pygame.image.load('boss/me_sp/me_sp.png')\
                .convert_alpha()
            self.image2 = pygame.image.load('boss/me_sp/me_sp2.png')\
                .convert_alpha()
            self.mask = pygame.mask.from_surface(self.image1)
            self.destroy_images = [
                pygame.image.load('boss/me_sp/me_sp_down1.png')
                .convert_alpha(),
                pygame.image.load('boss/me_sp/me_sp_down2.png')
                .convert_alpha(),
                pygame.image.load('boss/me_sp/me_sp_down3.png')
                .convert_alpha(),
                pygame.image.load('boss/me_sp/me_sp_down4.png')
                .convert_alpha()
                ]

            self.shield = pygame.image.load('boss/me_sp/shield.png')\
                .convert_alpha()
            self.shield_rect = self.shield.get_rect()

            self.life_image = pygame.image.load('boss/me_sp/life_sp.png')\
                .convert_alpha()
            self.life_rect = self.life_image.get_rect()

            self.bomb_image = pygame.image.load('boss/me_sp/bomb.png')\
                .convert_alpha()
            self.bomb_rect = self.bomb_image.get_rect()
            self.bomb_font = pygame.font.Font('font/font.ttf', 48)
            self.bomb_images = [
                    pygame.image.load('boss/bomb_sp/bomb1.png'),
                    pygame.image.load('boss/bomb_sp/bomb2.png'),
                    pygame.image.load('boss/bomb_sp/bomb3.png'),
                    pygame.image.load('boss/bomb_sp/bomb4.png'),
                    pygame.image.load('boss/bomb_sp/bomb5.png'),
                    pygame.image.load('boss/bomb_sp/bomb6.png')
                ]
        else:
            self.image1 = pygame.image.load('images/me/me1.png')\
                .convert_alpha()
            self.image2 = pygame.image.load('images/me/me2.png')\
                .convert_alpha()
            self.mask = pygame.mask.from_surface(self.image1)
            self.destroy_images = [
                pygame.image.load('images/me/me_destroy_1.png')
                .convert_alpha(),
                pygame.image.load('images/me/me_destroy_2.png')
                .convert_alpha(),
                pygame.image.load('images/me/me_destroy_3.png')
                .convert_alpha(),
                pygame.image.load('images/me/me_destroy_4.png')
                .convert_alpha()
                ]

            self.shield = pygame.image.load('images/me/shield.png')\
                .convert_alpha()
            self.shield_rect = self.shield.get_rect()

            self.life_image = pygame.image.load('images/me/life.png')\
                .convert_alpha()
            self.life_rect = self.life_image.get_rect()

            self.bomb_image = pygame.image.load('images/me/bomb.png')\
                .convert_alpha()
            self.bomb_rect = self.bomb_image.get_rect()
            self.bomb_font = pygame.font.Font('font/font.ttf', 48)
            self.bomb_images = [
                    pygame.image.load('images/bomb/bomb1.png'),
                    pygame.image.load('images/bomb/bomb2.png'),
                    pygame.image.load('images/bomb/bomb3.png'),
                    pygame.image.load('images/bomb/bomb4.png'),
                    pygame.image.load('images/bomb/bomb5.png'),
                    pygame.image.load('images/bomb/bomb6.png')
                ]
