
charmap = {
    ' ': 0,
    '#': 1,
    '0': 2,
    '@': 3,
    '^': 4
}

def get_size(data):
    lines = data.strip('\n').split('\n')
    return max(map(lambda x: len(x), lines)), len(lines)
