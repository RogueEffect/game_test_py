
import re

from level import Level
from box import Box
from player import Player





def get_size(data):
    lines = data.split('\n')
    return max(len(x) for x in lines), len(lines)


def load_level(path, mirror_x=False, mirror_y=False):
    with open(path, encoding='utf-8') as f:
        data = f.read().strip('\n')
    width, height = get_size(data)
    tiles = [0] * (width * height)
    mobs = []
    player = None

    m = re.search(r'(?:\\|/)([^\\/]+).txt', path)
    title = m[1] if m else "untitled"
    if mirror_x or mirror_y:
        title += ' mirrored'

    lines = data.split('\n')
    if mirror_y:
        lines = lines[::-1]

    for y, line in enumerate(lines):
        if mirror_x:
            line = reversed(line)
        for x, ch in enumerate(line):
            if ch == ' ':
                continue
            if ch == '0':
                mobs.append(Box(x, y))
                tiles[x + y * width] = 2
            elif ch == '&':
                mobs.append(Box(x, y))
                tiles[x + y * width] = 3
            elif ch == '@':
                player = Player(x, y)
                tiles[x + y * width] = 2
            else:
                tiles[x + y * width] = charmap[ch]
    level = Level(width, height, title, tiles, mobs, player)
    return level
