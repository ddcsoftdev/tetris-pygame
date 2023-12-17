from settings import *  # noqa: F403
from tetris import Tetris
import sys


class GameInstance:
    def __init__(self):
        pg.init()
        pg.display.set_caption("MyTetris")
        self.screen = pg.display.set_mode(FIELD_RES)
        self.clock = pg.time.Clock()
        self.tetris = Tetris(self)

    def update(self):
        self.tetris.draw()
        self.clock.tick(FPS)  # noqa: F405

    def draw(self):
        self.screen.fill(color=FIELD_COLOR)
        self.tetris.draw()
        pg.display.flip()
    
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
    
    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            
if __name__ == '__main__':
    game = GameInstance()
    game.run()