from OpenGL.GL import *

from ducky.model import Model
from ducky.program import Program

class OutlineModelStencil(Model):

    def __init__(self):
        super(OutlineModelStencil, self).__init__()
        
        self.outline_program = Program()
        self.outline_program.load_files('shaders/outline_stencil.vert.glsl', 'shaders/outline_stencil.frag.glsl')

    def render(self, opaque, elapsed, camera, program):
        glClear(GL_STENCIL_BUFFER_BIT)

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
