from asyncio import transports
from random import randint
import pygame as pg
from worlddata import BASE, TILE

class Wall(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('.//Resources/wall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

# Portal to level sprite
class Portal(pg.sprite.Sprite):

    def __init__(self, pos, teleporty, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('.//Resources/force-field.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.image = pg.transform.scale(self.image, (200,100))

        self.player = teleporty

    def transport(self):
        if pg.sprite.spritecollideany(self, self.player) != None:
            level = '1'
            print(level)
    
    def update(self):
        transports()


# Player sprite and movement controls
class Player(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('.//Resources/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        
        self.direction = pg.math.Vector2()
        self.speed = 5

# Movement inputs for the player
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
        
# Math for position change
    def move(self,speed):
        self.rect.center += self.direction * speed
            
# Updates the player sprite
    def update(self):
        self.moveControl()
        self.move(self.speed)

class BaseLogic():

    def __init__(self):
        
        self.display_surface = pg.display.get_surface()
# Creates sprite groups
        self.players = pg.sprite.Group()
        self.wall_group = pg.sprite.Group()

        self.makeSprites()

    def makeSprites(self):
        self.player = Player((0,0), self.players)
        for self.row_index,row in enumerate(BASE):
            for self.col_index,col in enumerate(row):
                x = self.col_index * TILE
                y = self.row_index * TILE
                if col == 'x':
                    Wall((x,y), self.wall_group)

                if col == 'z':
                    Portal((x,y), self.player, self.wall_group)

                if col == 'p':
                    self.player.rect.x = x
                    self.player.rect.y = y

    def scroll(self):

        if self.player.rect.x >= 1000:
            scroll = self.player.rect.x - 1000
            self.player.rect.x = 1000
            for p in self.wall_group:
                p.rect.x -= scroll

        if self.player.rect.x <= 10:
            scroll = 10 - self.player.rect.x
            self.player.rect.x = 10
            for p in self.wall_group:
                p.rect.x += scroll

        if self.player.rect.y >= 800:
            scroll = self.player.rect.y - 800
            self.player.rect.y = 800
            for p in self.wall_group:
                p.rect.y -= scroll

        if self.player.rect.y <= 10:
            scroll = 10 - self.player.rect.y
            self.player.rect.y = 10
            for p in self.wall_group:
                p.rect.y += scroll

    def run(self):
        self.players.update()
        self.scroll()
        self.wall_group.update()
        self.players.draw(self.display_surface)
        self.wall_group.draw(self.display_surface)