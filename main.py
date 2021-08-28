
import os

import pygame

from lvl_util import load_level


TITLE       = "Game Test"
WIDTH       = 360
HEIGHT      = 300
SCALE       = 2
FPS         = 60
FONT_SIZE   = 48

files = sorted(os.listdir('lvl_txt'))


class GameTest:
    """Game class"""
    def __init__(self):
        pygame.display.set_caption(TITLE)
        self.disp = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
        pygame.key.set_repeat(200, 200)
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.lvln = 0
        self.level = self.get_level(self.lvln)
        self.player = self.level.player
        self.moves = 0
        self.font = None
        self.font_size = 8 * SCALE
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

        self.player.tick()

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.mod & pygame.KMOD_CTRL and event.key == pygame.K_q:
                    self.running = False
                    return

                if event.key == pygame.K_r:
                    self.change_level(self.lvln)
                if event.key == pygame.K_COMMA:
                    if self.lvln != 0:
                        self.lvln -= 1
                        self.change_level(self.lvln)
                if event.key == pygame.K_PERIOD:
                    if self.lvln != len(files) - 1:
                        self.lvln += 1
                        self.change_level(self.lvln)

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    if self.player.move(self.level, 0, -1):
                        self.moves += 1
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    if self.player.move(self.level, -1, 0):
                        self.moves += 1
                if event.key in (pygame.K_s, pygame.K_DOWN):
                    if self.player.move(self.level, 0, 1):
                        self.moves += 1
                if event.key in (pygame.K_d, pygame.K_RIGHT):
                    if self.player.move(self.level, 1, 0):
                        self.moves += 1

            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        """Draw to the screen"""
        self.screen.fill((0, 0, 0))
        xo = (WIDTH - self.player.x * 32) // 2 - 8
        yo = (HEIGHT - self.player.y * 32) // 2 - 8
        self.level.render(self.screen, xo, yo)
        self.player.render(self.screen, (WIDTH - 16) // 2, (HEIGHT - 16) // 2)

        self.disp.blit(pygame.transform.scale(self.screen, (WIDTH * SCALE, HEIGHT * SCALE)), (0, 0))
        self.draw_text(self.disp, f'Moves: {self.moves}', 8, HEIGHT * SCALE - self.font_size)
        pygame.display.flip()

    def draw_text(self, surface, msg, x, y):
        """Draw some text"""
        if not self.font:
            raise Exception("Font not initialized")
        text = self.font.render(msg, True, 0xffffffff)
        surface.blit(text, (x, y))

    def get_level(self, id):
        return load_level(f'lvl_txt/{files[id]}')

    def change_level(self, id):
        self.level = self.get_level(id)
        self.player = self.level.player
        self.moves = 0


if __name__ == '__main__':
    game = GameTest()
    game.run()
    print('goodbye')
