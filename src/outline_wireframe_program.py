from OpenGL.GL import *

from ducky.program import Program

class OutlineWireframeProgram(Program):

    def __init__(self, main_program, line_width):
        super(OutlineWireframeProgram, self).__init__()
        self.main_program = main_program
        self.line_width = line_width

    def load_uniform_locations(self, gl_program):
        super(OutlineWireframeProgram, self).load_uniform_locations(gl_program)

        # MVP
        self.uModel =                       glGetUniformLocation(gl_program, 'uModel')
        self.uProjectionView =              glGetUniformLocation(gl_program, 'uProjectionView')

    def render_model(self, model, opaque, elapsed, camera):
        glClear(GL_STENCIL_BUFFER_BIT)

        glEnable(GL_STENCIL_TEST)
        glStencilFunc(GL_ALWAYS, 0x01, 0x01)
        glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
        glStencilMask(0x01)

        self.main_program.render_model(model, opaque, elapsed, camera)

        glStencilFunc(GL_EQUAL, 0, 0x01)
        glStencilMask(0x00)
        glLineWidth(self.line_width)
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

        self.use()
        glUniformMatrix4fv(self.uModel, 1, GL_FALSE, model.model.astype('float32').tobytes())
        glUniformMatrix4fv(self.uProjectionView, 1, GL_FALSE, camera.projection_view.astype('float32').tobytes())
        self.main_program.render_meshmtls(self.render_meshmtl, model, opaque)

        glDisable(GL_STENCIL_TEST)
        glStencilMask(0xFF)
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

    def render_meshmtl(self, meshmtl):
        glBindVertexArray(meshmtl.mesh.vao)
        glDrawArrays(GL_TRIANGLES, 0, len(meshmtl.mesh.faces) * 3)
