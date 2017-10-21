from OpenGL.GL import *

from ducky.app import app
from ducky.program import Program

class OutlineScaleConstantProgram(Program):

    def __init__(self, main_program, line_size, use_pixels):
        super(OutlineScaleConstantProgram, self).__init__()
        self.main_program = main_program
        self.line_size = line_size
        self.use_pixels = use_pixels

    def load_uniform_locations(self, gl_program):
        super(OutlineScaleConstantProgram, self).load_uniform_locations(gl_program)

        # MVP
        self.uModel =                       glGetUniformLocation(gl_program, 'uModel')
        self.uTransposeInverseModel =       glGetUniformLocation(gl_program, 'uTransposeInverseModel')
        self.uView =                        glGetUniformLocation(gl_program, 'uView')
        self.uProjection =                  glGetUniformLocation(gl_program, 'uProjection')

        self.uOutlineWidth =                glGetUniformLocation(gl_program, 'uOutlineWidth')
        self.uOutlineHeight =               glGetUniformLocation(gl_program, 'uOutlineHeight')

    def render_model(self, model, opaque, elapsed, camera):
        glClear(GL_STENCIL_BUFFER_BIT)

        glEnable(GL_STENCIL_TEST)
        glStencilFunc(GL_ALWAYS, 0x01, 0x01)
        glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
        glStencilMask(0x01)

        self.main_program.render_model(model, opaque, elapsed, camera)

        glDepthMask(GL_FALSE)
        glStencilFunc(GL_EQUAL, 0, 0x01)
        glStencilMask(0x00)

        line_width = self.line_size
        line_height = self.line_size
        if self.use_pixels:
            # Calculate pixel size in clip space
            px_width = (1.0 / app.width) * 2.0
            line_width = px_width * self.line_size
            px_height = (1.0 / app.height) * 2.0
            line_height = px_height * self.line_size

        self.use()
        glUniformMatrix4fv(self.uModel, 1, GL_FALSE, model.model.astype('float32').tobytes())
        glUniformMatrix4fv(self.uView, 1, GL_FALSE, camera.view.astype('float32').tobytes())
        glUniformMatrix4fv(self.uProjection, 1, GL_FALSE, camera.projection.astype('float32').tobytes())
        model_view = camera.view * model.model
        glUniformMatrix4fv(self.uTransposeInverseModel, 1, GL_FALSE, model_view.inverse.transpose().astype('float32').tobytes())
        glUniform1f(self.uOutlineWidth, line_width)
        glUniform1f(self.uOutlineHeight, line_height)
        self.main_program.render_meshmtls(self.render_meshmtl, model, opaque)

        glDepthMask(GL_TRUE)
        glDisable(GL_STENCIL_TEST)
        glStencilMask(0xFF)

    def render_meshmtl(self, meshmtl):
        glBindVertexArray(meshmtl.mesh.vao)
        glDrawArrays(GL_TRIANGLES, 0, len(meshmtl.mesh.faces) * 3)
