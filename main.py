
import pygame


TITLE   = "Game Test"
WIDTH   = 512
HEIGHT  = 480
FPS     = 30


class GameTest:
    def __init__(self):
        pygame.display.set_caption(TITLE)
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
    
    def run(self):
        while self.running:
            self.tick()
            self.render()
        pygame.quit()

    def tick(self):
        self.clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    print('w pressed')
                if event.key == pygame.K_a:
                    print('a pressed')
                if event.key == pygame.K_s:
                    print('s pressed')
                if event.key == pygame.K_d:
                    print('d pressed :(')
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    print(f'left click pressed at {event.pos}')
                if event.button == 3:
                    print(f'right click pressed at {event.pos}')
            
            if event.type == pygame.QUIT:
                self.running = False

    def render(self):
        self.win.fill((0, 0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    game = GameTest()
    game.run()
    print('done')
