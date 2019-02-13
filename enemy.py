# -*- coding:utf-8 -*-
"""
These are the enemy objects of the game.
Author: yanyongyu
"""

__author__ = "yanyongyu"
__all__ = ["SmallEnemy", "MidEnemy", "BigEnemy"]

import random

import pygame


class SmallEnemy(pygame.sprite.Sprite):
    score = 1000

    def __init__(self, bg_size, destroy_images):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/enemies/enemy1.png')\
            .convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.destroy_index = 0
        self.destroy_images = destroy_images

        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.rect.left = random.randint(0, self.width - self.rect.width)
        self.rect.top = random.randint(-5*self.height, 0)

        self.active = True
        self.energy = 1

        self.speed = 2

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left = random.randint(0, self.width - self.rect.width)
        self.rect.top = random.randint(-5*self.height, 0)


class MidEnemy(pygame.sprite.Sprite):
    energy = 8
    score = 6000

    def __init__(self, bg_size, destroy_images):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/enemies/enemy2.png')\
            .convert_alpha()
        self.image_hit = pygame.image.load('images/enemies/enemy2_hit.png')\
            .convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.destroy_index = 0
        self.destroy_images = destroy_images

        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.rect.left = random.randint(0, self.width - self.rect.width)
        self.rect.top = random.randint(-10*self.height, -self.height)

        self.active = True
        self.energy = MidEnemy.energy
        self.energy_color = None
        self.hit = False

        self.speed = 1

        self.score = 6000

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = MidEnemy.energy
        self.rect.left = random.randint(0, self.width - self.rect.width)
        self.rect.top = random.randint(-10*self.height, -self.height)


class BigEnemy(pygame.sprite.Sprite):
    energy = 20
    score = 10000

    def __init__(self, bg_size, destroy_images):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load('images/enemies/enemy3_n1.png')\
            .convert_alpha()
        self.image2 = pygame.image.load('images/enemies/enemy3_n2.png')\
            .convert_alpha()
        self.image_hit = pygame.image.load('images/enemies/enemy3_hit.png')\
            .convert_alpha()
        self.mask = pygame.mask.from_surface(self.image1)

        self.destroy_index = 0
        self.destroy_images = destroy_images

        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size
        self.rect.left = random.randint(0, self.width - self.rect.width)
        self.rect.top = random.randint(-15*self.height, -5*self.height)

        self.active = True
        self.energy = BigEnemy.energy
        self.energy_color = None
        self.hit = False

        self.speed = 1

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = BigEnemy.energy
        self.rect.left = random.randint(0, self.width - self.rect.width)
        self.rect.top = random.randint(-15*self.height, -5*self.height)
