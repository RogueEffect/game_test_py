
"""Box entities that can be pushed"""

from dirs import dirs
from mob import Mob
from tile_sheet import TileSheet

MOVE_FRAMES = 6
MOVEPX = 16 / MOVE_FRAMES

class Box(Mob):
    """Box entity"""
    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        self.sheet = TileSheet("res/box.png", 16, 16, True)

    def render(self, surface, xoffset, yoffset):
        yo, xo = 0, 0
        if self.move_time:
            dx, dy = dirs[(self.dir + 2) % 4]
            yo += MOVEPX * (MOVE_FRAMES - self.move_time) * -dy + 16 * dy
            xo += MOVEPX * (MOVE_FRAMES - self.move_time) * -dx + 16 * dx
        self.sheet.draw_tile(surface, xoffset + self.x * 16 + xo, yoffset + self.y * 16 + yo, 0)

    def passable(self):
        return False

    def push(self, level, dir):
        dx, dy = dirs[dir]
        return self.move(level, dx, dy)
