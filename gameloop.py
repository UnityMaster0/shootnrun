import sys
import time
import pygame as pg

from base import BaseLogic
from level import Logic

class gameContoller:

    def __init__(self):
        
        pg.init()
        self.screen = pg.display.set_mode((1680, 1080))
        pg.display.set_caption('ShootnRun')
        self.clock = pg.time.Clock()
        pg.mouse.set_cursor(*pg.cursors.diamond)

        self.logic = BaseLogic()

        self.atBase = True

        global start_time
        start_time = time.time()
        self.fps = 60

# Runs the game
    def run(self):
        while True:
            self.clock.tick(self.fps)
            for event in pg.event.get():
                if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()    
            self.screen.fill('darkgrey')
            self.logic.run()

        #Changes the level that is loaded
            if self.atBase == True:
                self.switchTo = self.logic.levelSet()
                if self.switchTo == 1:
                    self.logic = Logic(1)
                    self.atBase = False
                elif self.switchTo == 2:
                    self.logic = Logic(2)
                    self.atBase = False
                elif self.switchTo == 3:
                    self.logic = Logic(3)
                    self.atBase = False
    
            if pg.key.get_pressed()[pg.K_LSHIFT]:
                self.fps = 20
            else: self.fps = 60
            end_time = time.time()
            pg.display.update()

#Starts game loop
if __name__ == '__main__':
    game = gameContoller()
    game.run()