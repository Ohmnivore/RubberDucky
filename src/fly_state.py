from state import State
from model import Model
from OpenGL.GL import *
from OpenGL.GL import shaders

class FlyState(State):

    def __init__(self):
        vertex_shader_src = ''
        with open('shaders/vertex.glsl') as vertex_file:
            vertex_shader_src = vertex_file.read()
        vertex_shader = shaders.compileShader(vertex_shader_src, GL_VERTEX_SHADER)

        fragment_shader_src = ''
        with open('shaders/fragment.glsl') as fragment_file:
            fragment_shader_src = fragment_file.read()
        fragment_shader = shaders.compileShader(fragment_shader_src, GL_FRAGMENT_SHADER)

        self.shader = shaders.compileProgram(vertex_shader, fragment_shader)

        self.char = Model()
        # self.char.loadObj('assets/low poly girl/low poly girl.obj')
        self.char.loadObj('assets/triangle/triangle.obj')

    def update(self):
        pass

    def render(self):
        glDisable(GL_CULL_FACE)
        glUseProgram(self.shader)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        # glMatrixMode(GL_PROJECTION)
        # glOrtho(0, 1280, 0, 720, -1, 1)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.char.render()
        glUseProgram(0)
