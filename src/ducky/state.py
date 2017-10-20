from OpenGL.GL import *

class State:

    def __init__(self):
        self.entities = []

    def create(self):
        pass

    def update(self, elapsed):
        for entity in self.entities:
            entity.update(elapsed)

    def pre_render(self, elapsed):
        for entity in self.entities:
            entity.pre_render(elapsed)

    def render(self, elapsed, camera, program):
        pass
    
    def destroy(self):
        for entity in self.entities:
            entity.destroy()
