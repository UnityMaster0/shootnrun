import sys
import time

import pygame as pg

from base import BaseLogic
from level1 import LevelOneLogic
from level2 import LevelTwoLogic
from level3 import LevelThreeLogic

#FPS = 60

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
        global end_time
        while True:
            self.clock.tick(self.fps)
            for event in pg.event.get():
                if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
                    print('YOU SURVIVED FOR ', end_time - start_time, 'SECONDS')
                    pg.quit()
                    sys.exit()
                     
            self.screen.fill('darkgrey')
            self.logic.run()

        #Changes the level that is loaded
            if self.atBase == True:
                self.switchToOne = self.logic.levelSetOne()
                self.switchToTwo = self.logic.levelSetTwo()
                self.switchToThree = self.logic.levelSetThree()
                if self.switchToOne == True:
                    self.logic = LevelOneLogic()
                    self.atBase = False
                if self.switchToTwo == True:
                    self.logic = LevelTwoLogic()
                    self.atBase = False
                if self.switchToThree == True:
                    self.logic = LevelThreeLogic()
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