
import pygame

from lvl_util import load_level


TITLE       = "Game Test"
WIDTH       = 300
HEIGHT      = 240
SCALE       = 2
FPS         = 30
FONT_SIZE   = 24

level = load_level("lvl_txt/001.txt")
player = level.player


class GameTest:
    def __init__(self):
        pygame.display.set_caption(TITLE)
        self.disp = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
        pygame.key.set_repeat(200, 200)
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = None
        pygame.font.init()
        if pygame.font and pygame.font.get_init():
            self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.running = True


    def run(self):
        while self.running:
            self.tick()
            self.render()
        pygame.quit()

    def tick(self):
        self.clock.tick(FPS)

        player.tick()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    player.move(level, 0, -1)
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    player.move(level, -1, 0)
                if event.key in (pygame.K_s, pygame.K_DOWN):
                    player.move(level, 0, 1)
                if event.key in (pygame.K_d, pygame.K_RIGHT):
                    player.move(level, 1, 0)
                level.mob_at(player.x, player.y)
            """
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    print(f'left click pressed at {event.pos}')
                if event.button == 3:
                    print(f'right click pressed at {event.pos}')
            """
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        self.screen.fill((0, 0, 0))
        xo = (WIDTH - player.x * 32) // 2 - 8
        yo = (HEIGHT - player.y * 32) // 2 - 8
        level.render(self.screen, xo, yo)
        player.render(self.screen, (WIDTH - 16) // 2, (HEIGHT - 16) // 2)

        self.draw_text(self.screen, "Hello, world!", 16, 16)

        self.disp.blit(pygame.transform.scale(self.screen, (WIDTH * SCALE, HEIGHT * SCALE)), (0, 0))
        pygame.display.flip()

    def draw_text(self, surface, msg, x, y):
        if not self.font: raise Exception("Font not initialized")
        text = self.font.render(msg, True, 0xffffffff)
        surface.blit(text, (x, y))


if __name__ == '__main__':
    game = GameTest()
    game.run()
    print('done')
