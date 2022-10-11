from random import randint
import sys
from re import X
import time
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
['x',' ',' ','z',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','z',' ',' ','x'],
['x',' ',' ','z',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','z',' ',' ','x'],
['x',' ','e','z',' ',' ',' ',' ',' ',' ',' ',' ','p',' ',' ',' ',' ',' ',' ',' ',' ',' ','z','e',' ','x'],
['x',' ',' ','z',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','z',' ',' ','x'],
['x',' ',' ','z',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','z',' ',' ','x'],
['x','x','x','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x','x','x','x'],
[' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
[' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
[' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
[' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' '],
[' ',' ',' ','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x',' ',' ',' ']
]


# Wall sprite
class Wall(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('/home/adam/Programs/ShootnRun/Resources/wall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

class Forcefield(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('/home/adam/Programs/ShootnRun/Resources/force-field.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)


# Player sprite and movement controls
class Player(pg.sprite.Sprite):

    def __init__(self, pos, enemy, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('/home/adam/Programs/ShootnRun/Resources/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        
        self.direction = pg.math.Vector2()
        self.speed = 5

        self.enemy = enemy

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

    def collide(self):
        if pg.sprite.spritecollideany(self, self.enemy) != None:
            pg.quit()
            sys.exit()
            
    
    def update(self, dt):
        self.moveControl()
        self.move(self.speed)
        self.collide()


# Enemy sprite
class Enemy(pg.sprite.Sprite):

    def __init__(self, pos, target,*groups):
        super().__init__(*groups)
        self.image = pg.image.load('/home/adam/Programs/ShootnRun/Resources/enemy.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pg.math.Vector2()
        self.speed = randint(min_speed,max_speed)

        self.target = target

    # Makes enemies follow the player
    # Still need to fix               
    def update(self, dt):
        if self.target:
            self.direction = pg.math.Vector2(self.target.rect.center) - pg.math.Vector2(self.rect.center)
            if self.direction.length() > 0:
                self.direction.normalize_ip()
                self.rect.center += (self.direction * self.speed)


# Bullet class
class Bullet(pg.sprite.Sprite):

    def __init__(self, pos, target, killing, *groups):
        super().__init__(*groups)
 
        self.image = pg.image.load('/home/adam/Programs/ShootnRun/Resources/bullet.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.image = pg.transform.scale(self.image, (8,8))

        self.initial_pos = pg.math.Vector2(pos)
        self.target = pg.math.Vector2(target)
        self.speed = 20

        self.killing = killing

        self.direction = (self.target) - pg.math.Vector2(self.rect.center)
        if self.direction.length() > 0:
            self.direction.normalize_ip()
    
    def update(self, dt):
        self.rect.center += (self.direction * self.speed)
        
        v = self.initial_pos - pg.math.Vector2(self.rect.center)
        if v.length() > 500:
            self.kill()
        
        if pg.sprite.spritecollideany(self, self.killing) != None:
            pg.sprite.spritecollideany(self, self.killing).kill()
            self.kill()


class Gernade(pg.sprite.Sprite):

    def __init__(self, pos, target, killing, *groups):
        super().__init__(*groups)

        self.image = pg.image.load('/home/adam/Programs/ShootnRun/Resources/bullet.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.image = pg.transform.scale(self.image, (16,16))

        self.initial_pos = pg.math.Vector2(pos)
        self.target = pg.math.Vector2(target)
        self.speed = 20

        self.killing = killing

        self.direction = (self.target) - pg.math.Vector2(self.rect.center)
        if self.direction.length() > 0:
            self.direction.normalize_ip()
    
    def update(self, dt):
        self.rect.center += (self.direction * self.speed)
        
        v = self.initial_pos - pg.math.Vector2(self.rect.center)
        if v.length() > 500:
            self.kill()
        
        if pg.sprite.spritecollideany(self, self.killing) != None:
            pg.sprite.spritecollideany(self, self.killing).kill()


class Ammobox(pg.sprite.Sprite):

    def __init__(self, pos, count, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('/home/adam/Programs/ShootnRun/Resources/ammobox.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.count = count

    def pickup(self):
        self.count = 200
            

        
# Creates game sprites and logic
class Logic:
    
    def __init__(self):
        
        self.display_surface = pg.display.get_surface()

        self.players = pg.sprite.Group()
        self.wall_group = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.gernade = pg.sprite.Group()
        self.ammobox = pg.sprite.Group()

        self.makeSprites()

        self.ammo = 100 * 10
        self.gernade_supply = 5 * 10

    
    # Draws sprites
    def makeSprites(self):
        self.player = Player((0,0), self.enemies ,self.players)
        for self.row_index,row in enumerate(WORLD):
            for self.col_index,col in enumerate(row):
                x = self.col_index * TILE
                y = self.row_index * TILE
                if col == 'x':
                    Wall((x,y),[self.wall_group])

                if col == 'z':
                    Forcefield((x,y), self.wall_group)

                if col == 'p':
                    self.player.rect.x = x
                    self.player.rect.y = y

                if col == 'e':
                    tick = pg.time.get_ticks()
                    for spwan_enemies in range(2,6):
                        Enemy((x,y), self.player, self.enemies)

    def trigger(self):
        
        if self.mouse_button == (True, False, False):
                self.fire = pg.time.get_ticks()
                self.ammo -= 1
    
    def shoot(self):

        y = self.player.rect.y + 32
        x = self.player.rect.x + 32
  
        self.mouse_button = pg.mouse.get_pressed(num_buttons=3)

        try:
            if self.ammo >= 0:
                self.trigger()
                firing = pg.time.get_ticks() - self.fire
                if firing > 0 and firing < 18:    
                    Bullet((x,y), pg.mouse.get_pos(), self.enemies, self.bullets)

        except:
            return

    def windup_throw(self):
        
        if self.mouse_button == (False, False, True):
                self.throw = pg.time.get_ticks()
                self.gernade_supply -= 1
    
    def throw_gernade(self):

        y = self.player.rect.y + 32
        x = self.player.rect.x + 32
  
        self.mouse_button = pg.mouse.get_pressed(num_buttons=3)

        try:
            if self.gernade_supply >= 0:
                self.windup_throw()
                throwing = pg.time.get_ticks() - self.throw
                if throwing > 0 and throwing < 18:    
                    Gernade((x,y), pg.mouse.get_pos(), self.enemies, self.gernade)

        except:
            return

    def respawn_enemies(self):
        x1 = 23 * 64
        x2 = 2 * 64
        y = 8 * 64

        respawn = randint(1, diff_spawn)

        if respawn == 2:
            Enemy((x1,y), self.player, self.enemies)
        if respawn == 5:
            Enemy((x2,y), self.player, self.enemies)

    def spawn_ammo(self):

        x = randint(4, 21) * 64
        y = randint(2, 17) * 64

        if self.mouse_button == (False, True, False):
            Ammobox((x,y), self.ammo, self.ammobox)

                        
    def run(self, dt):
        self.shoot()
        self.throw_gernade()
        self.respawn_enemies()
        self.spawn_ammo()
        self.players.update(dt)
        self.enemies.update(dt)
        self.bullets.update(dt)
        self.wall_group.draw(self.display_surface)
        self.players.draw(self.display_surface)
        self.enemies.draw(self.display_surface)
        self.bullets.draw(self.display_surface)
        self.gernade.draw(self.display_surface)
        self.ammobox.draw(self.display_surface)

FPS = 60

class gameContoller:

    def __init__(self):
        
        pg.init()
        self.screen = pg.display.set_mode((1680, 1080))
        pg.display.set_caption('ShootnRun')
        self.clock = pg.time.Clock()
        self.logic = Logic()

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if pg.key.get_pressed()[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()
            
            self.screen.fill('darkgrey')
            self.logic.run(dt)
            pg.display.update()

global diff_spawn, max_speed, min_speed
diff_input = int(input('Set diffculty: '))

if diff_input == 1:
    diff_spawn = 80
    max_speed = 4
    min_speed = 2

if diff_input == 2:
    diff_spawn = 40
    max_speed = 5
    min_speed = 3

if diff_input == 3:
    diff_spawn = 30
    max_speed = 7
    min_speed = 4

#Starts game loop
if __name__ == '__main__':
    game = gameContoller()
    game.run()
