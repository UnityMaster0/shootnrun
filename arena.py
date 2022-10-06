import pygame as pg
from enemy import Enemy
from player import Player

running = True

#Sets size of WORLD sprites
TILE = 64

#Creates starting placement of sprites
WORLD = [
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x',' ',' ',' '],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x','x','x','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','p',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','e',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x','x','x','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x',' ',' ',' ']
]

#Defines the wall sprite
class Wall(pg.sprite.Sprite):

    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pg.image.load('/Volumes/2025/ajmunc25/Documents/Personal-Projects/Downloads/ShootNRun-main/Resources/wall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

#Draw the starting game sprites
class Arena:
    
    def __init__(self):
        
        self.display_surface = pg.display.get_surface()
        self.player_sprites = pg.sprite.Group()
        self.barrier_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()

        self.makeSprites()
    
    #Draws sprites
    def makeSprites(self):
        for row_index,row in enumerate(WORLD):
            for col_index,col in enumerate(row):
                x = col_index * TILE
                y = row_index * TILE
                if col == 'x':
                    Wall((x,y),[self.player_sprites,self.barrier_sprites])
                if col == 'p':
                    self.player = Player((x,y),[self.player_sprites],self.barrier_sprites)
                if col == 'e':
                    self.enemy = Enemy((x,y),[self.player_sprites],self.barrier_sprites)
                

    def run(self):
        self.barrier_sprites.draw(self.display_surface)
        self.player_sprites.draw(self.display_surface)
        self.enemy_sprites.draw(self.display_surface)
        self.player_sprites.update()
