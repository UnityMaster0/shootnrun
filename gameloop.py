import pygame as pg
import time
import sys
from main import LevelOneLogic
from base import BaseLogic

#FPS = 60

level = "b"


class gameContoller:

    def __init__(self):
        
        pg.init()
        self.screen = pg.display.set_mode((1680, 1080))
        pg.display.set_caption('ShootnRun')
        self.clock = pg.time.Clock()

        if level == "b":
            self.logic = BaseLogic()

        if level == "1":
            self.logic = LevelOneLogic()

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
            if pg.key.get_pressed()[pg.K_LSHIFT]:
                self.fps = 20
            else: self.fps = 60
            end_time = time.time()
            pg.display.update()

#Starts game loop
if __name__ == '__main__':
    game = gameContoller()
    game.run()