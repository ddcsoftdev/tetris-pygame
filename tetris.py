from settings import *
from tetromino import Tetromino
import math
import pygame.freetype as ft


class Text:
    def __init__(self, game):
        self.game = game
        self.font = ft.Font(FONT_PATH)
    
    def draw(self):
        self.font.render_to(self.game.screen, (WINDOW_W * 0.6, WINDOW_H * 0.03),
                            text = "TETRIS", fgcolor='black',
                            size = TILE_SIZE * 1.65, bgcolor='white')
        self.font.render_to(self.game.screen, (WINDOW_W * 0.65, WINDOW_H * 0.2),
                            text = "next", fgcolor='blue',
                            size = TILE_SIZE * 1.4, bgcolor='white')
        self.font.render_to(self.game.screen, (WINDOW_W * 0.64, WINDOW_H * 0.67),
                            text = "score", fgcolor='black',
                            size = TILE_SIZE * 1.4, bgcolor='white')
        self.font.render_to(self.game.screen, (WINDOW_W * 0.7, WINDOW_H * 0.8),
                            text = "000", fgcolor='green',
                            size = TILE_SIZE * 1.4, bgcolor='white')
        
        
class Tetris:
    def __init__(self, game):
        self.game = game
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.speed_up = False
        
        self.score = 0
        self.full_lines = 0
        self.points_per_line = {0: 0, 1: 100, 2: 250, 3: 500, 4: 1200}
    
    def check_full_lines(self):
        row = FIELD_H - 1
        for y in range(FIELD_H - 1, -1, -1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]
                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)
                    
            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
            else:
                for x in range(FIELD_W):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0
        
    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block
        
    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]
    
    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[0]:
            pg.time.wait(300)
            return True
    def check_tetromino_landed(self):
        if self.tetromino.landed:
            if self.is_game_over():
                self.__init__(self.game)
            else:
                self.speed_up = False
                self.put_tetromino_blocks_in_array()
                self.field_array
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)
        
    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetromino.move(direction='left')
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move(direction='right')
        elif pressed_key == pg.K_UP:
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True
            
    def control_cancel(self, pressed_key):
        if pressed_key == pg.K_DOWN:
            self.speed_up = False          

    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.game.screen, 'grey',
                             (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)
    def update(self):
        trigger = [self.game.anim_trigger, self.game.anim_trigger_fast][self.speed_up]
        if trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landed()
        self.sprite_group.update()
    
    def draw (self):
        self.draw_grid()
        self.sprite_group.draw(self.game.screen)