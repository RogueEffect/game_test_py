
from mob import Mob
from tile_sheet import TileSheet

class Box(Mob):
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.sheet = TileSheet("res/box.png", 16, 16, True)

    def render(self, surface, xoffset, yoffset):
        self.sheet.draw_tile(surface, xoffset + self.x * 16, yoffset + self.y * 16, 0)

    def passable(self):
        return False

    def push(self, level, dir):
        dx, dy = 0, 0
        if   dir == 0: dy = -1
        elif dir == 1: dx = 1
        elif dir == 2: dy = 1
        elif dir == 3: dx = -1
        return self.move(level, dx, dy)
