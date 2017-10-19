from OpenGL.GL import *

class State:

    def __init__(self):
        self.entities = []

    def create(self):
        pass

    def update(self, elapsed):
        for entity in self.entities:
            entity.update(elapsed)

    def render(self, elapsed, camera, program):
        # Opaque render pass first, then transparent
        for entity in self.entities:
            entity.render(True, elapsed, camera, program)

        glDepthMask(GL_FALSE)
        glEnable(GL_CULL_FACE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        for entity in self.entities:
            entity.render(False, elapsed, camera, program)

        glDepthMask(GL_TRUE)
        glDisable(GL_CULL_FACE)
        glDisable(GL_BLEND)
    
    def destroy(self):
        for entity in self.entities:
            entity.destroy()
