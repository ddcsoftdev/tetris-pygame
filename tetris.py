from settings import *
from tetramino import Tetramino
import math


class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.tetramino = Tetramino(self)
        
    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'grey',
                             (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
    def update(self):
        self.tetramino.update()
        self.sprite_group.update()
    
    def draw (self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)