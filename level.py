import sys
import pygame as pg
from random import randint

from worlddata import MAP, DIFFSPAWNONE, DIFFSPAWNTWO, DIFFSPAWNTHREE, MAXSPEEDONE, MAXSPEEDTWO, MAXSPEEDTHREE, MINSPEEDONE, MINSPEEDTWO, MINSPEEDTHREE, TILE

# Wall sprite
class Wall(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('.//Resources/wall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

# Forcefield sprite
class Forcefield(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('.//Resources/force-field.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

# Player sprite and movement controls
class Player(pg.sprite.Sprite):

    def __init__(self, pos, enemy, wall, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('.//Resources/player-left(4).png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        
        self.direction = pg.math.Vector2()
        self.speed = 5

        self.value = 0
        self.animation_images_left = [pg.image.load('.//Resources/player-left(1).png'), pg.image.load('.//Resources/player-left(2).png'),
                                pg.image.load('.//Resources/player-left(3).png'), pg.image.load('.//Resources/player-left(4).png')]
                            
        self.animation_images_right = [pg.image.load('.//Resources/player-right(2).png'), pg.image.load('.//Resources/player-right(1).png'),
                                pg.image.load('.//Resources/player-right(1).png'), pg.image.load('.//Resources/player-right(3).png')]
    
        self.enemy = enemy
        self.wall = wall

    # Movement inputs for the player
    def moveControl(self):
    
        if pg.sprite.spritecollideany(self, self.wall) != None:

            if self.locked_s == False and pg.key.get_pressed()[pg.K_w] == True:
                self.locked_w = True
                self.direction.y = 0
            elif self.locked_w == False and pg.key.get_pressed()[pg.K_w] == True:
                self.direction.y = -1
            elif self.locked_w == True and pg.key.get_pressed()[pg.K_w] == True:
                self.direction.y = 0

            if self.locked_w == False and pg.key.get_pressed()[pg.K_s] == True:
                self.locked_s = True
                self.direction.y = 0
            elif self.locked_s == False and pg.key.get_pressed()[pg.K_s] == True:
                self.direction.y = 1
            elif self.locked_s == True and pg.key.get_pressed()[pg.K_s] == True:
                self.direction.y = 0

            if self.locked_d == False and pg.key.get_pressed()[pg.K_a] == True:
                self.locked_a = True
                self.direction.x = 0
            elif self.locked_a == False and pg.key.get_pressed()[pg.K_a] == True:
                self.direction.x = -1
            elif self.locked_a == True and pg.key.get_pressed()[pg.K_a] == True:
                self.direction.x = 0

            if self.locked_a == False and pg.key.get_pressed()[pg.K_d] == True and pg.sprite.spritecollideany(self, self.wall) != None:
                self.locked_d = True
                self.direction.x = 0
            elif self.locked_d == False and pg.key.get_pressed()[pg.K_d] == True:
                self.direction.x = 1
            elif self.locked_d == True and pg.key.get_pressed()[pg.K_d] == True:
                self.direction.x = 0

        else:
            self.locked_w = False
            self.locked_s = False
            self.locked_a = False
            self.locked_d = False

            if pg.key.get_pressed()[pg.K_w] == True and pg.sprite.spritecollideany(self, self.wall) == None:
                self.direction.y = -1
            elif pg.key.get_pressed()[pg.K_s] == True and pg.sprite.spritecollideany(self, self.wall) == None:
                self.direction.y = 1
            else:
                self.direction.y = 0
        
            if pg.key.get_pressed()[pg.K_d] == True and pg.sprite.spritecollideany(self, self.wall) == None:
                self.direction.x = 1
            elif pg.key.get_pressed()[pg.K_a] == True and pg.sprite.spritecollideany(self, self.wall) == None:
                self.direction.x = -1
            else:
                self.direction.x = 0
        
    # Math for position change
    def move(self,speed):
        self.rect.center += self.direction * speed

    def animation(self):
    
        if pg.key.get_pressed()[pg.K_w]:
            self.value += 1

            if self.value >= len(self.animation_images_left):
                self.value = 0

            self.image = self.animation_images_left[self.value]

        if pg.key.get_pressed()[pg.K_s]:
            self.value += 1

            if self.value >= len(self.animation_images_right):
                self.value = 0

            self.image = self.animation_images_right[self.value]

        if pg.key.get_pressed()[pg.K_a]:
            self.value += 1

            if self.value >= len(self.animation_images_left):
                self.value = 0

            self.image = self.animation_images_left[self.value]


        if pg.key.get_pressed()[pg.K_d]:
            self.value += 1

            if self.value >= len(self.animation_images_right):
                self.value = 0

            self.image = self.animation_images_right[self.value]

    # Collision with enemy ends the game
    def collide(self):
        if pg.sprite.spritecollideany(self, self.enemy) != None:
            pg.quit()
            sys.exit()
            
    # Updates the player sprite
    def update(self):
        self.moveControl()
        self.move(self.speed)
        self.animation()
        self.collide()


# Enemy sprite
class Enemy(pg.sprite.Sprite):

    def __init__(self, pos, target, min_speed, max_speed, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('.//Resources/enemy.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pg.math.Vector2()
        self.speed = randint(min_speed, max_speed)

        self.target = target

    # Makes enemies follow the player        
    def update(self):
        if self.target:
            self.direction = pg.math.Vector2(self.target.rect.center) - pg.math.Vector2(self.rect.center)
            if self.direction.length() > 0:
                self.direction.normalize_ip()
                self.rect.center += (self.direction * self.speed)

# Bullet class
class Bullet(pg.sprite.Sprite):

    def __init__(self, pos, target, killing, *groups):
        super().__init__(*groups)
 
        self.image = pg.image.load('.//Resources/bullet.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.image = pg.transform.scale(self.image, (8,8))

        self.initial_pos = pg.math.Vector2(pos)
        self.target = pg.math.Vector2(target)
        self.speed = 20

        self.killing = killing

        self.direction = (self.target) - pg.math.Vector2(self.rect.center)

        if self.direction.length() > 0:
            self.direction.normalize_ip()

    # Math for bullet position change  
    def update(self):
        self.rect.center += (self.direction * self.speed)
        
        v = self.initial_pos - pg.math.Vector2(self.rect.center)
        if v.length() > 500:
            self.kill()
        
        if pg.sprite.spritecollideany(self, self.killing) != None:
            pg.sprite.spritecollideany(self, self.killing).kill()
            self.kill()

# Rocket sprite
class Rocket(pg.sprite.Sprite):

    def __init__(self, pos, target, killing, *groups):
        super().__init__(*groups)

        self.image = pg.image.load('.//Resources/bullet.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.image = pg.transform.scale(self.image, (16,16))

        self.initial_pos = pg.math.Vector2(pos)
        self.target = pg.math.Vector2(target)
        self.speed = 20

        self.killing = killing

        self.direction = (self.target) - pg.math.Vector2(self.rect.center)
        if self.direction.length() > 0:
            self.direction.normalize_ip()

    # Updates Rocket sprites
    def update(self):
        self.rect.center += (self.direction * self.speed)
        
        v = self.initial_pos - pg.math.Vector2(self.rect.center)
        if v.length() > 500:
            self.kill()
        
        if pg.sprite.spritecollideany(self, self.killing) != None:
            pg.sprite.spritecollideany(self, self.killing).kill()

class Portal(pg.sprite.Sprite):

    def __init__(self, pos, player, *groups):
        super().__init__(*groups)
        self.image = pg.image.load('.//Resources/force-field.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.image = pg.transform.scale(self.image, (200,100))

        self.player = player

# Creates game sprites and logic
class Logic:
    
    def __init__(self, select):
        
        self.display_surface = pg.display.get_surface()
        # Creates sprite groups
        self.players = pg.sprite.Group()
        self.wall_group = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.Rocket = pg.sprite.Group()
        self.ammobox = pg.sprite.Group()
        self.portal = pg.sprite.Group()

        self.makeSprites()

        if select == 1:
            self.diff_spawn = DIFFSPAWNONE
            self.max_speed = MAXSPEEDONE
            self.min_speed = MINSPEEDONE
        if select == 2:
            self.diff_spawn = DIFFSPAWNTWO
            self.max_speed = MAXSPEEDTWO
            self.min_speed = MINSPEEDTWO
        if select == 3:
            self.diff_spawn = DIFFSPAWNTHREE
            self.max_speed = MAXSPEEDTHREE
            self.min_speed = MINSPEEDTHREE

        self.Rocket_supply = 50
        self.onePortal = False

    # Draws sprites
    def makeSprites(self):
        self.player = Player((0,0), self.enemies, self.wall_group, self.players)
        for self.row_index,row in enumerate(MAP):
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

    # Checks that the trigger button is pressed and does timing
    def trigger(self):

        self.mouse_button = pg.mouse.get_pressed(num_buttons=3)
        
        if self.mouse_button == (True, False, False) or pg.key.get_pressed()[pg.K_SPACE] == True:
                self.fire = pg.time.get_ticks()
                
    # Shoots a bullet
    def shoot(self):

        y = self.player.rect.y + 32
        x = self.player.rect.x + 32

        try:
            self.trigger()
            firing = pg.time.get_ticks() - self.fire
            if firing > 0 and firing < 19:    
                Bullet((x,y), pg.mouse.get_pos(), self.enemies, self.bullets)

        except:
            return

    # Checks that the throw Rocket button is pressed and does timing
    def windup_throw(self):
        
        if self.mouse_button == (False, False, True):
                self.throw = pg.time.get_ticks()
                self.Rocket_supply -= 1

    # Throws the Rocket
    def throw_Rocket(self):

        y = self.player.rect.y + 32
        x = self.player.rect.x + 32
  
        self.mouse_button = pg.mouse.get_pressed(num_buttons=3)

        try:
            if self.Rocket_supply > 0:
                self.windup_throw()
                throwing = pg.time.get_ticks() - self.throw
                if throwing > 0 and throwing < 18:    
                    Rocket((x,y), pg.mouse.get_pos(), self.enemies, self.Rocket)

        except:
            return

    # Creates new eneimes randomly at spawn points
    def respawn_enemies(self):
        x = randint(1, 38) * 64
        y = randint(1,16) * 64

        respawn = randint(1, self.diff_spawn)

        if respawn == 1 or respawn == 2:
            Enemy((x,y), self.player, self.min_speed, self.max_speed, self.enemies)

    def scroll(self):

        if self.player.rect.x >= 1500:
            scroll = self.player.rect.x - 1500
            self.player.rect.x = 1500
            for w in self.wall_group:
                w.rect.x -= scroll
            for e in self.enemies:
                e.rect.x -= scroll

        if self.player.rect.x <= 100:
            scroll = 100 - self.player.rect.x
            self.player.rect.x = 100
            for w in self.wall_group:
                w.rect.x += scroll
            for e in self.enemies:
                e.rect.x += scroll

        if self.player.rect.y >= 800:
            scroll = self.player.rect.y - 800
            self.player.rect.y = 800
            for w in self.wall_group:
                w.rect.y -= scroll
            for e in self.enemies:
                e.rect.y -= scroll

        if self.player.rect.y <= 100:
            scroll = 100 - self.player.rect.y
            self.player.rect.y = 100
            for w in self.wall_group:
                w.rect.y += scroll
            for e in self.enemies:
                e.rect.y += scroll

    def summon_portal(self):

        if pg.key.get_pressed()[pg.K_p] and self.onePortal == False:
            xy = randint(1, 30) * 64
            Portal((xy,xy), self.player, self.portal)
            self.onePortal = True

    # Runs all game functions            
    def run(self):
        self.shoot()
        self.throw_Rocket()
        self.respawn_enemies()
        self.scroll()
        self.players.update()
        self.enemies.update()
        self.bullets.update()
        self.Rocket.update()
        self.wall_group.draw(self.display_surface)
        self.players.draw(self.display_surface)
        self.enemies.draw(self.display_surface)
        self.bullets.draw(self.display_surface)
        self.Rocket.draw(self.display_surface)