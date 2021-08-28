
from tile_sheet import TileSheet

sheet = TileSheet("res/tiles.png", 16, 16)

class Level:
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.tiles = [0] * (width * height)
        self.player = None
        self.mobs = []

    def set_tile(self, x, y, tile):
        self.tiles[x + y * self.WIDTH] = tile

    def get_tile(self, x, y):
        if x < 0 or y < 0: return -1
        if x >= self.WIDTH or y >= self.HEIGHT: return -1
        return self.tiles[x + y * self.WIDTH]

    def can_pass(self, x, y):
        return self.get_tile(x, y) != 1

    def mob_at(self, x, y):
        for mob in self.mobs:
            if (x, y) == (mob.x, mob.y):
                return mob

    def print_tiles(self):
        """DEBUG"""
        for y in range(self.HEIGHT):
            print(self.tiles[y * self.WIDTH:self.WIDTH + y * self.WIDTH])

    def tick(self):
        pass

    def render(self, surface, xoffset=0, yoffset=0):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                tile = self.tiles[x + y * self.WIDTH] - 1
                sheet.draw_tile(surface, xoffset + x * 16, yoffset + y * 16, tile)

        for mob in self.mobs:
            mob.render(surface, xoffset, yoffset)
