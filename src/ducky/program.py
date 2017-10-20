from OpenGL.GL import *
from OpenGL.GL import shaders

class Program:

    def __init__(self):
        self.gl_program = None

    def load_files(self, vertex_path, fragment_path):
        vertex_shader_src = ''
        with open(vertex_path) as vertex_file:
            vertex_shader_src = vertex_file.read()
        vertex_shader = shaders.compileShader(vertex_shader_src, GL_VERTEX_SHADER)

        fragment_shader_src = ''
        with open(fragment_path) as fragment_file:
            fragment_shader_src = fragment_file.read()
        fragment_shader = shaders.compileShader(fragment_shader_src, GL_FRAGMENT_SHADER)

        gl_program = shaders.compileProgram(vertex_shader, fragment_shader)
        self.gl_program = gl_program

        self.load_uniform_locations(self.gl_program)

    def use(self):
        glUseProgram(self.gl_program)

    def load_uniform_locations(self, gl_program):
        pass
