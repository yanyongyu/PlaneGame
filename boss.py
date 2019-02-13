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

    def __init__(self, bg_size, transitional_image, destroy_image):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('boss/lv1/lv1.png').convert_alpha()
        self.image_hit = pygame.image.load('boss/lv1/lv1_hit.png')\
            .convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.background = pygame.image.load('boss/bgimages/bg1.jpg').convert()

        self.transitional_index = 0
        self.transitional_image = transitional_image

        self.destroy_index = 0
        self.destroy_image = destroy_image

        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.rect.left = (self.width - self.rect.width) // 2
        self.rect.top = -0.2*self.height

        self.active = True
        self.energy = Boss_lv1.energy
        self.energy_color = None
        self.hit = False

        self.move_in_speed = 1
        self.move_speed = random.randint(1, 3)
        self.move_direction = random.choice([-1, 1])

    def move_in(self):
        if self.rect.top < 53:
            self.rect.top += self.move_in_speed

    def move(self):
        if self.rect.top >= 53:
            if self.rect.left <= 0:
                self.move_direction = 1
                self.move_speed = random.randint(1, 3)
            elif self.rect.left >= self.width - self.rect.width:
                self.move_direction = -1
                self.move_speed = random.randint(1, 3)
            self.rect.left += self.move_direction * self.move_speed


class Boss_lv2(pygame.sprite.Sprite):
    energy = 200
    score = 20000

    def __init__(self, bg_size, transitional_image, destroy_image):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('boss/lv2/lv2.png').convert_alpha()
        self.image_hit = pygame.image.load('boss/lv2/lv2_hit.png')\
            .convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.background = pygame.image.load('boss/bgimages/bg2.jpg').convert()

        self.transitional_index = 0
        self.transitional_image = transitional_image

        self.destroy_index = 0
        self.destroy_image = destroy_image

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
        self.move_speed = random.randint(1, 5)
        self.move_direction = random.choice([-1, 1])

    def move_in(self):
        if self.rect.top < 53:
            self.rect.top += self.move_in_speed

    def move(self):
        if self.rect.top >= 53:
            if self.rect.left <= 0:
                self.move_direction = 1
                self.move_speed = random.randint(1, 5)
            elif self.rect.left >= self.width - self.rect.width:
                self.move_direction = -1
                self.move_speed = random.randint(1, 5)
            self.rect.left += self.move_direction * self.move_speed

            self.move_delay -= 1
            if not self.move_delay:
                self.move_delay = 50
                self.rect.top += 1


class Boss_lv3(pygame.sprite.Sprite):
    energy = 300
    score = 30000

    def __init__(self, bg_size, transitional_image, destroy_image):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('boss/lv3/lv3.png').convert_alpha()
        self.image_hit = pygame.image.load('boss/lv3/lv3_hit.png')\
            .convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.background = pygame.image.load('boss/bgimages/bg3.jpg').convert()

        self.transitional_index = 0
        self.transitional_image = transitional_image

        self.destroy_index = 0
        self.destroy_image = destroy_image

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
        self.move_speed = random.randint(1, 5)
        self.move_direction = random.choice([-1, 1])

    def move_in(self):
        if self.rect.top < 53:
            self.rect.top += self.move_in_speed

    def move(self):
        if self.rect.top >= 53:
            if self.rect.left <= 0:
                self.move_direction = 1
                self.move_speed = random.randint(1, 5)
            elif self.rect.left >= self.width - self.rect.width:
                self.move_direction = -1
                self.move_speed = random.randint(1, 5)
            self.rect.left += self.move_direction * self.move_speed

            self.move_delay -= 1
            if not self.move_delay:
                self.move_delay = 20
                self.rect.top += 1
