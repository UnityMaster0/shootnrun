import pygame as pg, sys
from arena import Arena

#Sets FPS constant
FPS = 60

#Creates the game loop
class gameLoop:

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

            self.screen.fill('darkgrey')
            self.arena.run()
            pg.display.update()
            self.clock.tick(FPS)

#Starts game loop
if __name__ == '__main__':
    loop = gameLoop()
    loop.run()
