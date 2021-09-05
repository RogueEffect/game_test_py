
"""Level class"""

from sys import stderr

from tile_sheet import TileSheet

sheet = TileSheet("res/tiles.png", 16, 16)

class Level:
    """Level containing a grid of tiles, list of mobs and player"""
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.title = ""
        self.tiles = [0] * (width * height)
        self.player = None
        self.mobs = []

    def set_tile(self, x, y, tile):
        """Set the tile at x, y to the given tile"""
        self.tiles[x + y * self.WIDTH] = tile

    def get_tile(self, x, y):
        """Return a tile from the grid or -1 if out of bounds"""
        if x < 0 or y < 0:
            return -1
        if x >= self.WIDTH or y >= self.HEIGHT:
            return -1
        return self.tiles[x + y * self.WIDTH]

    def can_pass(self, x, y):
        """Return True if a mob can move onto the given coordinates"""
        return self.get_tile(x, y) != 1

    def mob_at(self, x, y):
        """Return True if a mob exists at the given coordinates"""
        for mob in self.mobs:
            if (x, y) == (mob.x, mob.y):
                return mob
        return None

    def complete(self):
        box_tiles = [self.tiles[mob.x + mob.y * self.WIDTH] for mob in self.mobs]
        return set(box_tiles) == {3}

    def tick(self):
        """Update the level"""
        for mob in self.mobs:
            mob.tick()

    def render(self, surface, xoffset=0, yoffset=0):
        """Draw the level, mobs and onto surface"""
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                tile = self.tiles[x + y * self.WIDTH] - 1
                sheet.draw_tile(surface, xoffset + x * 16, yoffset + y * 16, tile)

        for mob in self.mobs:
            mob.render(surface, xoffset, yoffset)

    def validate(self):
        if not self.player:
            print(f'Invalid level! There is no player start', file=stderr)
        spaces = len([x for x in self.tiles if x == 3])
        if spaces == 0:
            print(f'Invalid level! There are 0 spaces and {len(self.mobs)} boxes', file=stderr)
            return
        elif len(self.mobs) == 0:
            print(f'Invalid level! There are 0 boxes and {spaces} spaces', file=stderr)
            return
        elif spaces != len(self.mobs):
            print(f'Invalid level! There are {spaces} spaces and {len(self.mobs)} boxes', file=stderr)
