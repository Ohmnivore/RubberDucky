from state import State
from model import Model

class FlyState(State):

    def __init__(self):
        self.char = Model()
        self.char.loadObj('assets/low poly girl.obj')

    def update(self):
        pass

    def render(self):
        pass
