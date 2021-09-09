
import os
import sys

import pygame

from box import Box
from dirs import dirs
from lvl_util import load_level
from move_history import MoveHistory

TITLE       = "Sokoban"
WIDTH       = 360
HEIGHT      = 300
SCALE       = 2
DWIDTH      = WIDTH * SCALE
DHEIGHT     = HEIGHT * SCALE
FPS         = 30
FONT_SIZE   = 48
DONE_TIME   = 80
MAX_HISTORY = 100
MOVE_FRAMES = 6
MOVEPX      = 16 / MOVE_FRAMES

files = sorted(os.listdir('lvl_txt'))

# TODO refactor

class GameTest:
    """Game class"""
    def __init__(self, mirrored, debug):
        pygame.display.set_caption(TITLE)
        self.disp = pygame.display.set_mode((DWIDTH, DHEIGHT))
        pygame.key.set_repeat(190, 190)
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.lvln = 0
        self.level = None
        self.title_time = 0
        self.mirrored = mirrored
        self.moves = 0
        self.font = None
        self.font_size = 8 * SCALE
        self.complete_time = 0
        self.xo = 0
        self.yo = 0
        self.move_time = 0
        self.move_history = MoveHistory(MAX_HISTORY)
        self.change_level(self.lvln)
        self.player = self.level.player
        self.undo_time = 0
        self.debug = debug
        pygame.font.init()
        if pygame.font and pygame.font.get_init():
            name = pygame.font.match_font('input')
            if name:
                self.font = pygame.font.Font(name, FONT_SIZE // 2)
                self.font_size = self.font.size("x")[1]
            else:
                self.font = pygame.font.SysFont(name, FONT_SIZE)
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
        self.clock.tick(FPS)
        self.level.tick()

        if self.title_time:
            self.title_time -= 1

        if self.move_time:
            self.move_time -= 1

        if self.complete_time:
            if self.complete_time == 1:
                if self.lvln == len(files) - 1:
                    self.lvln = 0
                else:
                    self.lvln += 1
                self.change_level(self.lvln)
                return
            self.complete_time -= 1
            return

        if self.undo_time:
            self.undo_time -= 1

        self.player.tick()

        for event in pygame.event.get():
            buttons = pygame.mouse.get_pressed()
            if buttons[0]:
                try:
                    self.xo = -(event.pos[0] - WIDTH // 2 * SCALE) // 2
                    self.yo = -(event.pos[1] - HEIGHT // 2 * SCALE) // 2
                except AttributeError:
                    pass

            if event.type == pygame.KEYUP:
                if event.mod & pygame.KMOD_CTRL and event.key == pygame.K_q:
                    self.running = False
                    return

                if event.key == pygame.K_r:
                    self.change_level(self.lvln)
                if event.key == pygame.K_COMMA:
                    if event.mod & pygame.KMOD_SHIFT:
                        self.lvln -= 10
                        if self.lvln < 0: self.lvln = 0
                        self.change_level(self.lvln)
                    if self.lvln != 0:
                        self.lvln -= 1
                        self.change_level(self.lvln)
                if event.key == pygame.K_PERIOD:
                    if event.mod & pygame.KMOD_SHIFT:
                        self.lvln += 10
                        if self.lvln >= len(files): self.lvln = len(files) - 1
                        self.change_level(self.lvln)
                    elif self.lvln != len(files) - 1:
                        self.lvln += 1
                        self.change_level(self.lvln)
                if self.debug and event.mod & pygame.KMOD_SHIFT and event.key == pygame.K_b:
                    x, y = dirs[self.player.dir]
                    x += self.player.x
                    y += self.player.y
                    if self.level.can_pass(x, y):
                        self.move_history.clear()
                        self.level.mobs.append(Box(x, y))
                if self.level.complete():
                    self.complete_time = DONE_TIME

            if event.type == pygame.KEYDOWN:
                if self.move_time < 4:
                    if event.key in (pygame.K_w, pygame.K_UP):
                        if self.player.move(self.level, 0, -1, self.move_history):
                            self.moves += 1
                            self.move_time = MOVE_FRAMES
                    if event.key in (pygame.K_a, pygame.K_LEFT):
                        if self.player.move(self.level, -1, 0, self.move_history):
                            self.moves += 1
                            self.move_time = MOVE_FRAMES
                    if event.key in (pygame.K_s, pygame.K_DOWN):
                        if self.player.move(self.level, 0, 1, self.move_history):
                            self.moves += 1
                            self.move_time = MOVE_FRAMES
                    if event.key in (pygame.K_d, pygame.K_RIGHT):
                        if self.player.move(self.level, 1, 0, self.move_history):
                            self.moves += 1
                            self.move_time = MOVE_FRAMES
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
        xo = (WIDTH - self.player.x * 32) // 2 - 8
        yo = (HEIGHT - self.player.y * 32) // 2 - 8
        if self.move_time:
            dx, dy = dirs[self.player.dir]
            yo += MOVEPX * (MOVE_FRAMES - self.move_time) * -dy + 16 * dy
            xo += MOVEPX * (MOVE_FRAMES - self.move_time) * -dx + 16 * dx
        self.level.render(self.screen, self.xo + xo, self.yo + yo)
        self.player.render(self.screen, self.xo + (WIDTH - 16) // 2, self.yo + (HEIGHT - 16) // 2)

        self.disp.blit(pygame.transform.scale(self.screen, (DWIDTH, DHEIGHT)), (0, 0))
        self.draw_text(self.disp, f'Moves: {self.moves}', 8, DHEIGHT - self.font_size, background=0)

        if self.title_time:
            self.draw_text(self.disp, self.level.title, background=0)

        if self.complete_time:
            msg = "Level Complete!"
            if self.lvln == len(files) - 1:
                msg = "You win!"
            rect = pygame.Rect((DWIDTH - 300)//2, (DHEIGHT - 60)//2, 300, 60)
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
                    rect.center=(DWIDTH//2, DHEIGHT//2)
                if val == 'bottom':
                    rect.center=(DWIDTH//2, DHEIGHT - rect.height)
            if key == 'background':
                rect2 = rect.copy()
                rect2.width += 32
                rect2.center = rect.center
                pygame.draw.rect(surface, val, rect2)
        surface.blit(text, rect)

    def get_level(self, id):
        return load_level(f'lvl_txt/{files[id]}', self.mirrored)

    def change_level(self, id):
        self.level = self.get_level(id)
        self.player = self.level.player
        self.moves = 0
        self.complete_time = 0
        self.title_time = 100
        self.xo, self.yo = 0, 0
        self.move_history.clear()
        self.move_time = 0

    def undo(self):
        if self.move_history:
            move = self.move_history.pop()
            dir_ = (move.dir_ + 2) % 4
            self.player.move(self.level, *dirs[dir_])
            self.player.dir = move.dir_
            if move.pushed:
                self.moves += 1
                move.pushed.move(self.level, *dirs[dir_])
        else:
            self.undo_time = 30


if __name__ == '__main__':
    game = GameTest('--mirrored' in sys.argv, '--debug' in sys.argv)
    game.run()
    print('goodbye')
