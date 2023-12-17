from settings import *
import random

#inherits from pg Sprite class
class Block(pg.sprite.Sprite):
    def __init__(self, tetramino, pos):
        self.tetramino = tetramino
        self.pos = vec(pos) + INIT_POS_OFFSET
        
        super().__init__(tetramino.tetris.sprite_group)
        self.image = pg.Surface([TILE_SIZE, TILE_SIZE])
        self.image.fill('green')
        self.rect = self.image.get_rect()
        
    def set_rect_post(self):
        self.rect.topleft = self.pos * TILE_SIZE
        
    def update(self):
        self.set_rect_post()


class Tetramino:
    def __init__(self, tetris):
        self.tetris = tetris
        self.shape = random.choice(list(TETRAMINOES.keys()))
        self.block = [Block(self, pos) for pos in TETRAMINOES[self.shape]]
    
    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        for block in self.blocks:
            block.pos += move_direction
            
    def update(self):
        self.move(direction='down')