from state import State
from model import Model
from OpenGL.GL import *
from OpenGL.GL import shaders

class FlyState(State):

    def __init__(self):
        super(FlyState, self).__init__()

        vertex_shader_src = ''
        with open('shaders/vertex.glsl') as vertex_file:
            vertex_shader_src = vertex_file.read()
        vertex_shader = shaders.compileShader(vertex_shader_src, GL_VERTEX_SHADER)

        fragment_shader_src = ''
        with open('shaders/fragment.glsl') as fragment_file:
            fragment_shader_src = fragment_file.read()
        fragment_shader = shaders.compileShader(fragment_shader_src, GL_FRAGMENT_SHADER)

        self.shader = shaders.compileProgram(vertex_shader, fragment_shader)

        self.girl = Model()
        self.entities.append(self.girl)
        self.girl.load_obj('assets/low poly girl/low poly girl.obj')
        self.girl.pos += [0.0, 0.0, 8.0]

        self.teapot = Model()
        self.entities.append(self.teapot)
        self.teapot.load_obj('assets/teapot/teapot.obj')
        self.teapot.pos += [-8.0, 0.0, 0.0]

        # self.triangle = Model()
        # self.entities.append(self.triangle)
        # self.triangle.load_obj('assets/triangle/triangle.obj')
        # self.triangle.pos += [8.0, 0.0, 0.0]

    def update(self, elapsed):
        super(FlyState, self).update(elapsed)

    def render(self, elapsed, camera):
        glUseProgram(self.shader)
        super(FlyState, self).render(elapsed, camera, self.shader)
        glUseProgram(0)

    def destroy(self):
        super(FlyState, self).destroy()
