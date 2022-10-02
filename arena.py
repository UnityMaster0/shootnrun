import pygame as pg

running = True

#Sets size of WORLD sprites
TILE = 64

#Creates starting placement of sprites
WORLD = [
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','p',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x']
]

#Defines the wall sprite
class Wall(pg.sprite.Sprite):

    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pg.image.load('/home/adam/Programs/ShootnRun/Resources/wall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

#Defines the player sprite
class Player(pg.sprite.Sprite):

    def __init__(self,pos,groups,barrier_sprites):
        super().__init__(groups)
        self.image = pg.image.load('/home/adam/Programs/ShootnRun/Resources/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pg.math.Vector2()
        self.speed = 10

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

#Draw the starting game sprites
class Arena:
    
    def __init__(self):
        
        self.display_surface = pg.display.get_surface()
        self.people_sprites = pg.sprite.Group()
        self.barrier_sprites = pg.sprite.Group()

        self.makeSprites()
    
    #Draws sprites
    def makeSprites(self):
        for row_index,row in enumerate(WORLD):
            for col_index,col in enumerate(row):
                x = col_index * TILE
                y = row_index * TILE
                if col == 'x':
                    Wall((x,y),[self.people_sprites,self.barrier_sprites])
                if col == 'p':
                    self.player = Player((x,y),[self.people_sprites],self.barrier_sprites)
                

    def run(self):
        self.barrier_sprites.draw(self.display_surface)
        self.people_sprites.draw(self.display_surface)
        self.people_sprites.update()
