
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
        
        # make a box (can use an object to contain this instead)
        self.bx = 64
        self.by = 64
        self.bsize = 96
        self.xspeed = 5
        self.yspeed = 5
        self.maxspeed = 10
    
    def run(self):
        while self.running:
            self.tick()
            self.render()
        pygame.quit()

    def tick(self): # responsible for everything but drawing
        self.clock.tick(FPS)
        
        # box movement logic
        self.bx += self.xspeed
        self.by += self.yspeed
        if(self.bx + self.bsize >= WIDTH):
            self.bx = WIDTH - self.bsize - 1
            self.xspeed *= -1
        if(self.bx < 0):
            self.bx = 0
            self.xspeed *= -1
        if(self.by < 0):
            self.by = 0
            self.yspeed *= -1
        if(self.by + self.bsize >= HEIGHT):
            self.by = HEIGHT - self.bsize - 1
            self.yspeed *= -1
        
        for event in pygame.event.get():
            # handle a key press
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    print('w pressed')
                if event.key == pygame.K_a:
                    print('a pressed')
                if event.key == pygame.K_s:
                    print('s pressed')
                if event.key == pygame.K_d:
                    print('d pressed :(')
            
            # handle mouse click
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    print(f'left click pressed at {event.pos}')
                if event.button == 3:
                    print(f'right click pressed at {event.pos}')
                
                # try to increase speed on mouse click
                self.xspeed += 1 if self.xspeed > 0 else -1
                self.yspeed += 1 if self.yspeed > 0 else -1
                # otherwise reset speed to 1
                if abs(self.xspeed) > self.maxspeed:
                    self.xspeed = self.xspeed // abs(self.xspeed)
                if abs(self.yspeed) > self.maxspeed:
                    self.yspeed = self.yspeed // abs(self.yspeed)
            
            if event.type == pygame.QUIT:
                self.running = False
        
    def render(self): # only drawing stuff happens here
        # clear background
        self.win.fill((0, 0, 0))
        # draw the box
        self.win.subsurface(self.bx, self.by, self.bsize, self.bsize).fill((0, 255, 0))
        # update display
        pygame.display.flip()


if __name__ == '__main__':
    game = GameTest()
    game.run()
    print('done')
