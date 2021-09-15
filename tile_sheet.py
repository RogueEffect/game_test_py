
"""TileSheet class"""

import pygame

class TileSheet:
    """Tile sheet to facilitate storing and drawing tiles"""
    def __init__(self, path, tile_width, tile_height, sprite=False):
        self.image = pygame.image.load(path)
        self.TWIDTH = tile_width
        self.THEIGHT = tile_height
        if sprite:
            self.image.set_colorkey(0xff00ff)
        self.tiles = []
        tiles_wide = self.image.get_width() // tile_width
        tiles_high = self.image.get_height() // tile_height
        for y in range(tiles_high):
            for x in range(tiles_wide):
                rect = pygame.Rect(x * tile_width, y * tile_height, tile_width, tile_height)
                self.tiles.append(self.image.subsurface(rect))

    def draw_tile(self, surface, x, y, tile):
        self.image.set_colorkey(None)
        if tile < 0 or tile >= len(self.tiles):
            return
        surface.blit(self.tiles[tile], (x, y))
