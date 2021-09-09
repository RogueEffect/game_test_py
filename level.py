
"""Level class"""

from sys import stderr

from dirs import dirs
from tile_sheet import TileSheet


VOID = 0
WALL = 1
FLOOR = 2
SPACE = 3

SHEET = TileSheet("res/tiles.png", 16, 16)
WALLS = TileSheet("res/tiles2.png", 16, 16)

# todo map connected list to image tile



class Level:
    """Level containing a grid of tiles, list of mobs and player"""
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height
        self.title = ""
        self.tiles = [0] * (width * height)
        self.ctiles = None
        self.player = None
        self.mobs = []

    def init(self, title):
        # TODO move into __init__ (change in lvl_util)
        self.title = title
        self.ctiles = self.connect_walls()

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
        return self.get_tile(x, y) != WALL

    def mob_at(self, x, y):
        """Return True if a mob exists at the given coordinates"""
        for mob in self.mobs:
            if (x, y) == (mob.x, mob.y):
                return mob
        return None

    def complete(self):
        """Return True if all boxes are on space tiles"""
        box_tiles = [self.tiles[mob.x + mob.y * self.WIDTH] for mob in self.mobs]
        return set(box_tiles) == {SPACE}

    def tick(self):
        """Update the level"""
        for mob in self.mobs:
            mob.tick()

    def render(self, surface, xoffset=0, yoffset=0):
        """Draw the level, mobs and onto surface"""
        tw = SHEET.TWIDTH
        th = SHEET.THEIGHT
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                tile = self.tiles[x + y * self.WIDTH] - 1
                if tile == WALL - 1:
                    tile = self.get_ctile(x, y)
                    WALLS.draw_tile(surface, xoffset + x * tw, yoffset + y * th, tile)
                else:
                    SHEET.draw_tile(surface, xoffset + x * tw, yoffset + y * th, tile)

        for mob in self.mobs:
            mob.render(surface, xoffset, yoffset)

    def connected_texture(self, x, y, connect_oob=False):
        """Calculate a texture number for the tile at x, y
        if connect_oob is True count out of bounds as connected"""
        if self.get_tile(x, y) != WALL:
            return -1
        texture = 0
        for i in range(4):
            dx, dy = dirs[i]
            tile = self.get_tile(x + dx, y + dy)
            if tile == WALL or (tile == -1 and connect_oob):
                texture |= 1 << i
        return texture

    def connect_walls(self):
        """Precalculate connected textures for walls"""
        ctiles = []
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                ctiles.append(self.connected_texture(x, y))
        return ctiles

    def get_ctile(self, x, y):
        """Get texture for connected walls"""
        # TODO merge with get_tile?
        if x < 0 or y < 0:
            return -1
        if x >= self.WIDTH or y >= self.HEIGHT:
            return -1
        return self.ctiles[x + y * self.WIDTH]


    def validate(self):
        """Print an error if a level is not solvable"""
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
