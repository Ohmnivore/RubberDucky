from OpenGL.GL import *
from OpenGL.GL import shaders

from ducky.model import Model
from ducky.program import Program

class OutlineModelStencil(Model):

    def __init__(self):
        super(OutlineModelStencil, self).__init__()

        vertex_shader_src = ''
        with open('shaders/outline_stencil.vert.glsl') as vertex_file:
            vertex_shader_src = vertex_file.read()
        vertex_shader = shaders.compileShader(vertex_shader_src, GL_VERTEX_SHADER)

        fragment_shader_src = ''
        with open('shaders/outline_stencil.frag.glsl') as fragment_file:
            fragment_shader_src = fragment_file.read()
        fragment_shader = shaders.compileShader(fragment_shader_src, GL_FRAGMENT_SHADER)

        gl_program = shaders.compileProgram(vertex_shader, fragment_shader)
        self.outline_program = Program(gl_program)

    def render(self, opaque, elapsed, camera, program):
        glEnable(GL_STENCIL_TEST)
        glStencilFunc(GL_ALWAYS, 0x01, 0x01)
        glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
        glStencilMask(0x01)

        super(OutlineModelStencil, self).render(opaque, elapsed, camera, program)

        glStencilFunc(GL_EQUAL, 0, 0x01)
        glStencilMask(0x00)
        glLineWidth(2)
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

        super(OutlineModelStencil, self).render(opaque, elapsed, camera, self.outline_program)

        glDisable(GL_STENCIL_TEST)
        glStencilMask(0xFF)
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
