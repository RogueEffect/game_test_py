
import random

import pygame

from mob import Mob

class AIMob(Mob):
    def __init__(self, boundRect):
        super().__init__()
        self.bounds = boundRect
        self.dx = 0
        self.dy = 0
        self.time = 90
        self.rtime = random.randint(0, 90)
        self.speed = 5
        self.color = 0x0000ff

    def move(self, dx, dy):
        # keep the ai mob in bounds
        # test one dir at a time so mob can slide against wall
        if not self.bounds.contains(self.rect.move(dx, 0)):
            dx = 0
        if not self.bounds.contains(self.rect.move(0, dy)):
            dy = 0
        self.rect.move_ip(dx, dy)

    def tick(self):
        super().tick()
        if self.tickcount % (self.time + self.rtime) == 0:
            self.rtime = random.randint(0, 60)
            self.dx = random.randint(0, 2) - 1
            self.dy = random.randint(0, 2) - 1
        # mob moves one pixel at a time several times in a row to avoid weird behavior near the edge
        for i in range(self.speed):
            self.move(self.dx, self.dy)
