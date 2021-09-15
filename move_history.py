
from collections import namedtuple

Move = namedtuple('Move', ['dir', 'pushed'])

class MoveHistory:
    def __init__(self, max_history):
        self.MAX_HISTORY = max_history
        self.history = []

    def add(self, move):
        self.history.append(Move(*move))
        if len(self.history) > self.MAX_HISTORY:
            self.history.pop(0)

    def pop(self):
        return self.history.pop(-1)

    def __len__(self):
        return len(self.history)

    def clear(self):
        self.history = []
