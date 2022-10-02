import pygame as pg

class Bullet(pg.sprite.Sprite):

    def __init__(self,pos,groups):
        
        super().__init__(groups)
        self.image = pg.image.load('/home/adam/Programs/ShootnRun/Resources/wall.png').convert_alpha()

        self.shoot(self)

    def shoot(self):
