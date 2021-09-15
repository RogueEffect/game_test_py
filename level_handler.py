
import os

from box import Box
from dirs import dirs
from level import Level
from player import Player


MIRROR_X = 1
MIRROR_Y = 2

charmap = {
    ' ': -1,
    '#': 1,
    '.': 2,
    '^': 3,
    '@': 2,
    '0': 2,
    '&': 3
}


class LevelHandler:
    def __init__(self, config):
        self.config = config
        self.level_files = self.get_level_files()
        self.level_num = 0
        self.level = self.load_level()
        self.player = self.level.player

    def get_level_files(self):
        path = self.config.levels_path
        return os.listdir(path)

    def next_level(self):
        self.adjust_level(1)

    def prev_level(self):
        self.adjust_level(-1)

    def adjust_level(self, n):
        self.level_num += n
        if self.level_num >= len(self.level_files) or self.level_num < 0:
            self.level_num = 0
        self.level = self.load_level()

    def set_level(self, n):
        self.level_num = n
        self.level = self.load_level()

    def load_level(self):
        path = self.level_path()
        with open(path, encoding='utf-8') as f:
            data = f.read().strip('\n')
        width, height = self.get_size(data)
        title = self.get_title(path)
        tiles = [-1] * (width * height)
        mobs = []
        player = None
        if self.config.mirror: # TODO if random, keep same flip until level change but not reset
            title += ' mirrored'
        lines = data.split('\n')
        if self.config.mirror & MIRROR_Y:
            lines = lines[::-1]
        for y, line in enumerate(lines):
            if self.config.mirror & MIRROR_X:
                line = reversed(line)
            for x, c in enumerate(line):
                tiles[x + y * width] = charmap[c]
                if c in '0&':
                    mobs.append(Box(x, y))
                if c == '@':
                    player = Player(x, y)
        self.player = player
        return Level(width, height, title, tiles, mobs, player)
        

    def level_path(self):
        filename = self.level_files[self.level_num]
        path = os.path.join(self.config.basepath, self.config.levels_path, filename)
        return path

    @staticmethod
    def get_size(data):
        lines = data.split('\n')
        height = len(lines)
        width = len(lines[0])
        return width, height

    @staticmethod
    def get_title(path):
        filename = os.path.basename(path)
        return filename.split('.')[0]

    def complete(self):
        return self.level.complete()

    def last_level(self):
        return self.level_num == len(self.level_files) - 1

    def tick(self):
        self.level.tick()
        self.player.tick()

    def render(self, surface, xoffset, yoffset):
        self.level.render(surface, xoffset, yoffset)

    def debug_add_box(self):
        x, y = dirs[self.player.dir]
        x += self.player.x
        y += self.player.y
        if self.level.can_pass(x, y):
            self.level.mobs.append(Box(x, y))
            return True
        return False
