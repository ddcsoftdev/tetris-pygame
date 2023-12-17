from settings import *
import random

#inherits from pg Sprite class
class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino
        self.pos = vec(pos) + INIT_POS_OFFSET
        self.alive = True
        
        super().__init__(tetromino.tetris.sprite_group)
        self.image = pg.Surface([TILE_SIZE, TILE_SIZE])
        pg.draw.rect(self.image, 'green', (1, 1, TILE_SIZE - 2, TILE_SIZE - 2), border_radius=2)
        self.rect = self.image.get_rect()
    
    def is_alive(self):
        if not self.alive:
            self.kill()

    def rotate(self, pivot_pos):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos
        
    def set_rect_pos(self):
        self.rect.topleft = self.pos * TILE_SIZE
        
    def update(self):
        self.is_alive()
        self.set_rect_pos()
    
    def is_colliding(self, pos) -> bool:
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < FIELD_W and y < FIELD_H and (
            y < 0 or not self.tetromino.tetris.field_array[y][x]):
            return False
        return True


class Tetromino:
    def __init__(self, tetris):
        self.tetris = tetris
        self.shape = random.choice(list(TETROMINOES.keys()))
        self.blocks = [Block(self, pos) for pos in TETROMINOES[self.shape]]
        self.landed = False
    
    def rotate(self):
        pivot_pos = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]
        
        if not self.is_colliding(new_block_positions):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]
        
    def is_colliding(self, block_position):
        return any(map(Block.is_colliding, self.blocks, block_position))
    
    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]
        is_colliding = self.is_colliding(new_block_positions)
        
        if not is_colliding:
            for block in self.blocks:
                block.pos += move_direction
        elif direction == 'down':
            self.landed = True
            
    def update(self):
        self.move(direction='down')
