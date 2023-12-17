from settings import *  # noqa: F403
from tetris import Tetris, Text
import sys
import pathlib


class GameInstance:
    def __init__(self):
        pg.init()
        pg.display.set_caption("MyTetris")
        self.screen = pg.display.set_mode(WINDOW_RES)
        self.clock = pg.time.Clock()
        self.set_timer()
        self.images = self.load_images()
        self.tetris = Tetris(self)
        self.text = Text(self)

    def load_images(self):
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
        return images
    
    def update(self):
        self.tetris.update()
        self.clock.tick(FPS)  # noqa: F405

    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.user_event_fast = pg.USEREVENT + 1
        self.anim_trigger = False
        self.anim_trigger_fast = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.user_event_fast, FAST_ANIM_TIME_INTERVAL)

    def draw(self):
        self.screen.fill(color=BG_COLOR)
        self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
        self.tetris.draw()
        self.text.draw()
        pg.display.flip()
            
    def check_events(self):
        self.anim_trigger = False
        self.anim_trigger_fast = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)
            elif event.type == pg.KEYUP:
                self.tetris.control_cancel(pressed_key=event.key)
            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.user_event_fast:
                self.anim_trigger_fast = True
    
    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            
if __name__ == '__main__':
    game = GameInstance()
    game.run()