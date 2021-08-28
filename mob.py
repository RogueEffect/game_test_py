
"""Mob class"""

from dirs import dirs

class Mob:
    """Mobile entity base class"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.dir = 2
        self.sheet = None

    def move(self, level, dx, dy):
        self.dir = dirs[(dx, dy)]
        dx += self.x
        dy += self.y
        if not level.can_pass(dx, dy):
            return False
        mob = level.mob_at(dx, dy)
        if mob:
            if not self.can_push():
                return False
            if not mob.push(level, self.dir):
                return False
        self.x, self.y = dx, dy
        return True

    def passable(self):
        return False

    def pushable(self):
        return False

    def can_push(self):
        return False

    def push(self, level, dir):
        return False

    def tick(self):
        ...

    def render(self, surface, xoffset, yoffset):
        ...
