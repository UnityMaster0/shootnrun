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

    def __init__(self, pos, player, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('.//Resources/force-field.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.image = pg.transform.scale(self.image, (200,100))

        self.player = player


# Player sprite and movement controls
class Player(pg.sprite.Sprite):

    def __init__(self, pos, wall, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('.//Resources/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        
        self.direction = pg.math.Vector2()
        self.speed = 5

        self.wall = wall
        self.locked = False

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

        if self.locked_w == False and pg.key.get_pressed()[pg.K_w] and pg.sprite.spritecollideany(self, self.wall) != None:
            self.locked_w = True
            self.direction.y = 0
        elif self.locked_w == False:

        if self.locked_s == False and pg.key.get_pressed()[pg.K_s] and pg.sprite.spritecollideany(self, self.wall) != None:
            self.locked_s = True
            self.direction.y = 0
        elif self.locked_s == False:


        if self.locked_s == False and pg.key.get_pressed()[pg.K_a] and pg.sprite.spritecollideany(self, self.wall) != None:
            self.locked_s = True
            self.direction.x = 0
        elif self.locked_s == False:

        if self.locked_a == False and pg.key.get_pressed()[pg.K_d] and pg.sprite.spritecollideany(self, self.wall) != None:
            self.locked_a = True
            self.direction.x = 0
        elif self.locked_w == False:

        if pg.sprite.spritecollideany(self, self.wall) == None:
            self.locked = False



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
        self.portal_group = pg.sprite.Group()

        self.makeSprites()

    def makeSprites(self):
        self.player = Player((0,0), self.wall_group, self.players)
        for self.row_index,row in enumerate(BASE):
            for self.col_index,col in enumerate(row):
                x = self.col_index * TILE
                y = self.row_index * TILE
                if col == 'x':
                    Wall((x,y), self.wall_group)

                if col == '1':
                    self.toLevelOne = Portal((x,y), self.players, self.portal_group)

                if col == '2':
                    self.toLevelTwo = Portal((x,y), self.players, self.portal_group)

                if col == '3':
                    self.toLevelThree = Portal((x,y), self.players, self.portal_group)

                if col == 'p':
                    self.player.rect.x = x
                    self.player.rect.y = y

    def scroll(self):

        if self.player.rect.x >= 1500:
            scroll = self.player.rect.x - 1500
            self.player.rect.x = 1500
            for w in self.wall_group:
                w.rect.x -= scroll
            for p in self.portal_group:
                p.rect.x -= scroll

        if self.player.rect.x <= 100:
            scroll = 100 - self.player.rect.x
            self.player.rect.x = 100
            for w in self.wall_group:
                w.rect.x += scroll
            for p in self.portal_group:
                p.rect.x += scroll

        if self.player.rect.y >= 800:
            scroll = self.player.rect.y - 800
            self.player.rect.y = 800
            for w in self.wall_group:
                w.rect.y -= scroll
            for p in self.portal_group:
                p.rect.y -= scroll

        if self.player.rect.y <= 100:
            scroll = 100 - self.player.rect.y
            self.player.rect.y = 100
            for w in self.wall_group:
                w.rect.y += scroll
            for p in self.portal_group:
                p.rect.y += scroll
                
    def run(self):
        self.players.update()
        self.scroll()
        self.wall_group.update()
        self.portal_group.update()
        self.players.draw(self.display_surface)
        self.wall_group.draw(self.display_surface)
        self.portal_group.draw(self.display_surface)

    '''Each of the setLevel... functions take a post condition of self and reutrn a posts condition of True.
    These functions check if the player is colliding with the one of the portals. Based on the portal that is collided with the function will return True respectivly
    The post conditon functions are used in gameloop.py to change the level that is loaded.'''

    def levelSetOne(self):
        if pg.sprite.spritecollideany(self.toLevelOne, self.players):
            return True
    
    def levelSetTwo(self):
        if pg.sprite.spritecollideany(self.toLevelTwo, self.players):
            return True

    def levelSetThree(self):
        if pg.sprite.spritecollideany(self.toLevelThree, self.players):
            return True   
