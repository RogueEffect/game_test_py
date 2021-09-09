
import re

from level import Level
from box import Box
from player import Player

charmap = {
    ' ': 0,
    '#': 1,
    '.': 2,
    '^': 3,
    '@': 4,
    '0': 5,
    '&': 6
}

def get_size(data):
    lines = data.split('\n')
    return max(map(lambda x: len(x), lines)), len(lines)

def load_level(path, mirrored=False):
    with open(path, encoding='utf-8') as f:
        data = f.read().strip('\n')
    # TODO move level initialization to after we get all the tiles from level file
    width, height = get_size(data)
    level = Level(width, height)

    m = re.search(r'(?:\\|/)([^\\/]+).txt', path)
    title = m[1] if m else "untitled"
    if mirrored:
        title += ' mirrored'

    for y, line in enumerate(data.split('\n')):
        if mirrored:
            line = reversed(line)
        for x, ch in enumerate(line):
            if ch == ' ':
                continue
            if ch == '0':
                level.mobs.append(Box(x, y))
                level.set_tile(x, y, 2)
            elif ch == '&':
                level.mobs.append(Box(x, y))
                level.set_tile(x, y, 3)
            elif ch == '@':
                level.player = Player(x, y)
                level.set_tile(x, y, 2)
            else:
                level.set_tile(x, y, charmap[ch])
    level.init(title)
    level.validate()
    return level
