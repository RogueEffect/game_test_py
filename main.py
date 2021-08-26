
import pygame

from ai_mob import AIMob
from player import Player


TITLE   = "Game Test"
WIDTH   = 768
HEIGHT  = 720
FPS     = 30

player = Player()
mob = AIMob(pygame.Rect(0, 0, WIDTH, HEIGHT))
mob.set_pos((200, 200))


class GameTest:
    def __init__(self):
        pygame.display.set_caption(TITLE)
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.key.set_repeat(1, 1)
        self.clock = pygame.time.Clock()
        self.running = True
    
    def run(self):
        while self.running:
            self.tick()
            self.render()
        pygame.quit()

    def tick(self): # responsible for everything but drawing
        self.clock.tick(FPS)
        
        # handle multiple keys down at once
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(0, -5)
        if keys[pygame.K_a]:
            player.move(-5, 0)
        if keys[pygame.K_s]:
            player.move(0, 5)
        if keys[pygame.K_d]:
            player.move(5, 0)
        
        for event in pygame.event.get():
            # handle mouse click
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    print(f'left click pressed at {event.pos}')
                    player.set_pos(event.pos)
                if event.button == 3:
                    print(f'right click pressed at {event.pos}')
            
            if event.type == pygame.QUIT:
                self.running = False
        
        mob.tick()
        
    def render(self): # only drawing stuff happens here
        # clear background
        self.win.fill((0, 0, 0))
        # draw the mob
        mob.render(self.win)
        # draw the player
        player.render(self.win)
        # update display
        pygame.display.flip()


if __name__ == '__main__':
    game = GameTest()
    game.run()
    print('done')
