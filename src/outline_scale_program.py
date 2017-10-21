from OpenGL.GL import *

from ducky.program import Program

class OutlineScaleProgram(Program):

    def __init__(self, main_program, line_width):
        super(OutlineScaleProgram, self).__init__()
        self.main_program = main_program
        self.line_width = line_width

    def load_uniform_locations(self, gl_program):
        super(OutlineScaleProgram, self).load_uniform_locations(gl_program)

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

        self.use()
        scale_backup = model.scale.xyz
        model.scale.xyz = [scale_backup.x * 1.1, scale_backup.y * 1.1, scale_backup.z * 1.1]
        model.compute_model_matrix(elapsed)
        glUniformMatrix4fv(self.uModel, 1, GL_FALSE, model.model.tolist())
        glUniformMatrix4fv(self.uProjectionView, 1, GL_FALSE, camera.projection_view.tolist())
        self.main_program.render_meshmtls(self.render_meshmtl, model, opaque)

        model.scale.xyz = scale_backup
        model.compute_model_matrix(elapsed)
        glDisable(GL_STENCIL_TEST)
        glStencilMask(0xFF)

    def render_meshmtl(self, meshmtl):
        glBindVertexArray(meshmtl.mesh.vao)
        glDrawArrays(GL_TRIANGLES, 0, len(meshmtl.mesh.faces) * 3)
