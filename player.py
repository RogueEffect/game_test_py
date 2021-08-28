
from tile_sheet import TileSheet
from mob import Mob

class Player(Mob):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.tickcount = 0
        self.sheet = TileSheet("res/player.png", 16, 16, True)

    def tick(self):
        self.tickcount += 1

    def render(self, surface, xoffset, yoffset):
        ty = self.tickcount % 20 // 10
        self.sheet.draw_tile(surface, xoffset, yoffset, self.dir + ty * 4)

    def can_push(self):
        return True
