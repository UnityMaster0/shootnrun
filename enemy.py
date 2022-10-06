import pygame as pg
from player import Player

class Enemy(pg.sprite.Sprite):

    def __init__(self,pos,groups,barrier_sprites):
        super().__init__(groups)
        self.image = pg.image.load('/Volumes/2025/ajmunc25/Documents/Personal-Projects/Downloads/ShootNRun-main/Resources/pixil-frame-0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.enemy_direction = pg.math.Vector2()
        self.speed = 4
    
#AttributeError: type object 'Player' has no attribute 'rect'

    def follow(self):
    
        if self.rect.y >= Player.rect.y:
            self.enemy_direction.y = -1
        else:
            self.enemy_direction.y = 0

        if self.rect.x >= Player.rect.x:
            self.enemy_direction.x = -1
        else:
            self.enemy_direction.x = 0

    def enemy_move(self,speed):
        self.rect.center += self.enemy_direction * speed

    def update(self):
        self.follow()
        self.enemy_move(self.speed)

