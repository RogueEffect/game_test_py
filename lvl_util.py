
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

def load_level(path):
    with open(path, encoding='utf-8') as f:
        data = f.read().strip('\n')
    width, height = get_size(data)
    level = Level(width, height)
    for y, line in enumerate(data.split('\n')):
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
    level.validate()
    return level
