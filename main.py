
import sys

import pygame

from config import Config
from dirs import dirs
from level_handler import LevelHandler
from move_history import MoveHistory


MOVE_KEYS = [pygame.K_w, pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT]


class GameTest:
    """Game class"""
    def __init__(self, mirror_x, mirror_y, debug):
        self.config = Config()
        self.movepx = 16 / self.config.move_frames
        if mirror_x or mirror_y:
            self.config.mirror = 0
            if mirror_x:
                self.config.mirror |= 1
            if mirror_y:
                self.config.mirror |= 2
        self.level_handler = LevelHandler(self.config)
        pygame.display.set_caption(self.config.title)
        self.dwidth = self.config.width * self.config.scale
        self.dheight = self.config.height * self.config.scale
        self.disp = pygame.display.set_mode((self.dwidth, self.dheight))
        pygame.key.set_repeat(self.config.key_repeat_delay, self.config.key_repeat_interval)
        self.screen = pygame.Surface((self.config.width, self.config.height))
        self.clock = pygame.time.Clock()
        self.title_time = 0
        self.moves = 0
        self.font = None
        self.font_size = 8 * self.config.scale
        self.complete_time = 0
        self.xo = 0
        self.yo = 0
        self.move_time = 0
        self.move_history = MoveHistory(self.config.max_history)
        self.undo_time = 0
        self.debug = debug
        pygame.font.init()
        if pygame.font and pygame.font.get_init():
            name = pygame.font.match_font('input')
            if name:
                self.font = pygame.font.Font(name, self.config.font_size // 2)
                self.font_size = self.font.size("x")[1]
            else:
                self.font = pygame.font.SysFont(name, self.config.font_size)
                self.font_size = self.font.size("x")[1]
        self.running = True


    def run(self):
        """Run the game"""
        while self.running:
            self.tick()
            self.render()
        pygame.quit()

    def tick(self):
        """Do updates"""
        self.clock.tick(self.config.fps)

        self.level_handler.tick()

        if self.title_time:
            self.title_time -= 1

        if self.move_time:
            self.move_time -= 1

        if self.complete_time:
            if self.complete_time == 1:
                self.level_handler.next_level()
                self.level_change()
                return
            self.complete_time -= 1
            return

        if self.undo_time:
            self.undo_time -= 1

        for event in pygame.event.get():
            buttons = pygame.mouse.get_pressed()
            if buttons[0]:
                try:
                    self.xo = -(event.pos[0] - self.config.width // 2 * self.config.scale) // 2
                    self.yo = -(event.pos[1] - self.config.height // 2 * self.config.scale) // 2
                except AttributeError:
                    pass

            if event.type == pygame.KEYUP:
                if event.mod & pygame.KMOD_CTRL and event.key == pygame.K_q:
                    self.running = False
                    return
                
                if event.key == pygame.K_r:
                    self.title_time = 100
                    self.level_handler.level = self.level_handler.load_level()
                    self.level_change()

                if event.key == pygame.K_COMMA:
                    if event.mod & pygame.KMOD_SHIFT:
                        self.level_handler.adjust_level(-10)
                        self.level_change()
                    else:
                        self.level_handler.prev_level()
                        self.level_change()
                if event.key == pygame.K_PERIOD:
                    if event.mod & pygame.KMOD_SHIFT:
                        self.level_handler.adjust_level(10)
                        self.level_change()
                    else:
                        self.level_handler.next_level()
                        self.level_change()
                if self.debug and event.mod & pygame.KMOD_SHIFT and event.key == pygame.K_b:
                    if self.level_handler.debug_add_box():
                        self.move_history.clear()

                if self.level_handler.complete():
                    self.complete_time = self.config.done_time

            if event.type == pygame.KEYDOWN:
                if event.key in MOVE_KEYS and self.move_time < 4:
                    self.handle_move(MOVE_KEYS.index(event.key) % 4)
                    
                if event.mod & pygame.KMOD_CTRL and event.key == pygame.K_z:
                    self.undo()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.xo, self.yo = 0, 0

            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        """Draw to the screen"""
        self.screen.fill((0, 0, 0))
        xo = (self.config.width - self.level_handler.player.x * 32) // 2 - 8
        yo = (self.config.height - self.level_handler.player.y * 32) // 2 - 8
        if self.move_time:
            dx, dy = dirs[self.level_handler.player.dir]
            yo += self.movepx * (self.config.move_frames - self.move_time) * -dy + 16 * dy
            xo += self.movepx * (self.config.move_frames - self.move_time) * -dx + 16 * dx
        
        self.level_handler.render(self.screen, self.xo + xo, self.yo + yo)
        self.level_handler.player.render(self.screen, self.xo + (self.config.width - 16) // 2, self.yo + (self.config.height - 16) // 2)

        self.disp.blit(pygame.transform.scale(self.screen, (self.dwidth, self.dheight)), (0, 0))
        self.draw_text(self.disp, f'Moves: {self.moves}', 8, self.dheight - self.font_size, background=0)

        if self.title_time:
            self.draw_text(self.disp, self.level_handler.level.title, background=0)

        if self.complete_time:
            msg = "Level Complete!"
            if self.level_handler.last_level():
                msg = "You win!"
            rect = pygame.Rect((self.dwidth - 300) // 2, (self.dheight - 60) // 2, 300, 60)
            pygame.draw.rect(self.disp, 0, rect)
            self.draw_text(self.disp, msg, position='center')
        elif self.undo_time:
            msg = "Can't undo"
            self.draw_text(self.disp, msg, position='bottom', background=0)

        pygame.display.flip()

    def draw_text(self, surface, msg, x=0, y=0, **kwargs):
        """Draw some text"""
        if not self.font:
            raise Exception("Font not initialized")
        text = self.font.render(msg, True, 0xffffffff)
        rect = text.get_rect()
        rect.topleft = (x, y)
        for key, val in kwargs.items():
            if key == 'position':
                if val == 'center':
                    rect.center=(self.dwidth//2, self.dheight//2)
                if val == 'bottom':
                    rect.center=(self.dwidth//2, self.dheight - rect.height)
            if key == 'background':
                rect2 = rect.copy()
                rect2.width += 32
                rect2.center = rect.center
                pygame.draw.rect(surface, val, rect2)
        surface.blit(text, rect)

    def level_change(self):
        self.moves = 0
        self.complete_time = 0
        self.title_time = 100
        self.xo, self.yo = 0, 0
        self.move_history.clear()
        self.move_time = 0

    def undo(self):
        if self.move_history:
            move = self.move_history.pop()
            dir = (move.dir + 2) % 4
            self.level_handler.player.move(self.level_handler.level, *dirs[dir])
            self.level_handler.player.dir = move.dir
            if move.pushed:
                self.moves += 1
                move.pushed.move(self.level_handler.level, *dirs[dir])
        else:
            self.undo_time = 30

    def handle_move(self, dir):
        if self.level_handler.player.move(
            self.level_handler.level,
            *dirs[dir],
            self.move_history):
            self.moves += 1
            self.move_time = self.config.move_frames



if __name__ == '__main__':
    game = GameTest('--mirror_x' in sys.argv, '--mirror_y' in sys.argv, '--debug' in sys.argv)
    game.run()
    print('goodbye')
