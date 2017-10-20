from OpenGL.GL import *

from ducky.program import Program

class OutlineStencilProgram(Program):

    def __init__(self, main_program):
        super(OutlineStencilProgram, self).__init__()
        self.main_program = main_program

    def load_uniform_locations(self, gl_program):
        super(OutlineStencilProgram, self).load_uniform_locations(gl_program)

        # MVP
        self.uModel =                       glGetUniformLocation(gl_program, 'uModel')
        self.uProjectionView =              glGetUniformLocation(gl_program, 'uProjectionView')

        # Material uniforms
        self.uMaterial_ambientColor =       glGetUniformLocation(gl_program, 'uMaterial.ambientColor')
        self.uMaterial_diffuseColor =       glGetUniformLocation(gl_program, 'uMaterial.diffuseColor')
        self.uMaterial_specularColor =      glGetUniformLocation(gl_program, 'uMaterial.specularColor')
        self.uMaterial_specularExponent =   glGetUniformLocation(gl_program, 'uMaterial.specularExponent')
        self.uMaterial_alpha =              glGetUniformLocation(gl_program, 'uMaterial.alpha')
        self.uMaterial_emissiveColor =      glGetUniformLocation(gl_program, 'uMaterial.emissiveColor')

    def render_model(self, model, opaque, elapsed, camera):
        glClear(GL_STENCIL_BUFFER_BIT)

        glEnable(GL_STENCIL_TEST)
        glStencilFunc(GL_ALWAYS, 0x01, 0x01)
        glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
        glStencilMask(0x01)

        self.main_program.render_model(model, opaque, elapsed, camera)

        glStencilFunc(GL_EQUAL, 0, 0x01)
        glStencilMask(0x00)
        glLineWidth(2)
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )

        self.use()
        model.bind_essential_matrices(self, camera)
        model.render_meshmtls(opaque, self)

        glDisable(GL_STENCIL_TEST)
        glStencilMask(0xFF)
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
