from random import randint
import pygame as pg

#Sets size of each string
TILE = 64

#Creates starting placement of sprites
WORLD = [
[' ',' ',' ','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x',' ',' ',' '],
[' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
[' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
[' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
['x','x','x','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x','x','x','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ','e',' ',' ',' ',' ',' ',' ',' ',' ',' ','p',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','e',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x'],
['x','x','x','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x','x','x','x'],
[' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
[' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
[' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
[' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
[' ',' ',' ','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x',' ',' ',' ']
]


# Wall sprite
class Wall(pg.sprite.Sprite):

    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pg.image.load('/home/adam/Programs/ShootnRun/Resources/wall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)


# Player sprite and movement controls
class Player(pg.sprite.Sprite):

    def __init__(self,pos, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('/home/adam/Programs/ShootnRun/Resources/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        
        self.direction = pg.math.Vector2()
        self.speed = 5

    def moveControl(self):
    
        if self.rect.y >= 64:
            if self.rect.y <= 896:
                if pg.key.get_pressed()[pg.K_w]:
                    self.direction.y = -1
                elif pg.key.get_pressed()[pg.K_s]:
                    self.direction.y = 1
                else:
                    self.direction.y = 0
            else:
                self.direction.y = 0
                self.rect.y = 896
        else:
            self.direction.y = 0
            self.rect.y = 64

        if self.rect.x >= 254:
            if self.rect.x <= 1344:
                if pg.key.get_pressed()[pg.K_d]:
                    self.direction.x = 1
                elif pg.key.get_pressed()[pg.K_a]:
                    self.direction.x = -1
                else:
                    self.direction.x = 0
            else:
                self.direction.x = 0
                self.rect.x = 1344
        else:
            self.direction.x = 0
            self.rect.x = 254
        
        
    def move(self,speed):
        self.rect.center += self.direction * speed

    
    def update(self):
        self.moveControl()
        self.move(self.speed)


# Enemy sprite
class Enemy(pg.sprite.Sprite):

    def __init__(self, pos, target, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('/home/adam/Programs/ShootnRun/Resources/enemy.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pg.math.Vector2()
        self.speed = randint(1,4)

        self.target = target

    # Makes enemies follow the player
    # Still need to fix               
    def update(self):
        if self.target:
            self.direction = pg.math.Vector2(self.target.rect.center) - pg.math.Vector2(self.rect.center)
            if self.direction.length() > 0:
                self.direction.normalize_ip()
                self.rect.center += (self.direction * self.speed)

# Bullet class
class Bullet(pg.sprite.Sprite):

    def __init__(self, pos, target, *groups):
        super().__init__(*groups)
 
        self.image = pg.image.load('/home/adam/Programs/ShootnRun/Resources/wall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.image = pg.transform.scale(self.image, (8,8))

        self.initial_pos = pg.math.Vector2(pos)
        self.target = pg.math.Vector2(target)
        self.speed = 20

        self.direction = (self.target) - pg.math.Vector2(self.rect.center)
        if self.direction.length() > 0:
            self.direction.normalize_ip()
    
    def update(self):
        self.rect.center += (self.direction * self.speed)
        v = self.initial_pos - pg.math.Vector2(self.rect.center)
        if v.length() > 400:
            self.kill()


# Creates game sprites and logic
class Arena:
    
    def __init__(self):
        
        self.display_surface = pg.display.get_surface()
        self.player_sprites = pg.sprite.Group()
        self.wall_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()
        self.bullets = pg.sprite.Group()

        self.makeSprites()
    
    # Draws sprites
    def makeSprites(self):
        self.player = Player((0,0),[self.player_sprites])
        for row_index,row in enumerate(WORLD):
            for col_index,col in enumerate(row):
                x = col_index * TILE
                y = row_index * TILE
                if col == 'x':
                    Wall((x,y),[self.wall_sprites])
                if col == 'p':
                    self.player.rect.x = x
                    self.player.rect.y = y
                if col == 'e':
                    for spwan_enemies in range(0,1000):
                        Enemy((x,y), self.player, self.enemy_sprites)

    def shoot(self):

        y = self.player.rect.y + 32
        x = self.player.rect.x + 32
  
        self.mouse_button = pg.mouse.get_pressed(num_buttons=3)

        if self.mouse_button == (True, False, False):
            Bullet((x,y), pg.mouse.get_pos(), self.bullets)
            
            
    def run(self):
        self.shoot()
        self.player_sprites.update()
        self.enemy_sprites.update()
        self.bullets.update()
        self.wall_sprites.draw(self.display_surface)
        self.player_sprites.draw(self.display_surface)
        self.enemy_sprites.draw(self.display_surface)
        self.bullets.draw(self.display_surface)

import sys

FPS = 60

class gameContoller:

    def __init__(self):
        
        pg.init()
        self.screen = pg.display.set_mode((1680, 1080))
        pg.display.set_caption('ShootnRun')
        self.clock = pg.time.Clock()
        self.arena = Arena()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if pg.key.get_pressed()[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()

            self.screen.fill('darkgrey')
            self.arena.run()
            pg.display.update()
            self.clock.tick(FPS)

#Starts game loop
if __name__ == '__main__':
    loop = gameContoller()
    loop.run()
