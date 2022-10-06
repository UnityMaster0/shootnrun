import pygame as pg

#Defines the player sprite
class Player(pg.sprite.Sprite):

    def __init__(self,pos,groups,barrier_sprites):
        super().__init__(groups)
        self.image = pg.image.load('/Volumes/2025/ajmunc25/Documents/Personal-Projects/Downloads/ShootNRun-main/Resources/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        
        self.direction = pg.math.Vector2()
        self.speed = 5

    def moveControl(self):
    
        if pg.key.get_pressed()[pg.K_w]:
            self.direction.y = -1
        elif pg.key.get_pressed()[pg.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if pg.key.get_pressed()[pg.K_d]:
            self.direction.x = 1
        elif pg.key.get_pressed()[pg.K_a]:
            self.direction.x = -1
        else:
         self.direction.x = 0
        
    def move(self,speed):
        self.rect.center += self.direction * speed

    def update(self):
        self.moveControl()
        self.move(self.speed)