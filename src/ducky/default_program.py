from OpenGL.GL import *

from ducky.app import app
from ducky.program import Program

class DefaultProgram(Program):

    def load_uniform_locations(self, gl_program):
        super(DefaultProgram, self).load_uniform_locations(gl_program)

        # MVP
        self.uModel =                       glGetUniformLocation(gl_program, 'uModel')
        self.uTransposeInverseModel =       glGetUniformLocation(gl_program, 'uTransposeInverseModel')
        self.uProjectionView =              glGetUniformLocation(gl_program, 'uProjectionView')

        # Gamma
        self.uGamma =                       glGetUniformLocation(gl_program, 'uGamma')

        # View position
        self.uViewPosition =                glGetUniformLocation(gl_program, 'uViewPosition')

        # Material uniforms
        self.uMaterial_ambientColor =       glGetUniformLocation(gl_program, 'uMaterial.ambientColor')
        self.uMaterial_diffuseColor =       glGetUniformLocation(gl_program, 'uMaterial.diffuseColor')
        self.uMaterial_specularColor =      glGetUniformLocation(gl_program, 'uMaterial.specularColor')
        self.uMaterial_specularExponent =   glGetUniformLocation(gl_program, 'uMaterial.specularExponent')
        self.uMaterial_alpha =              glGetUniformLocation(gl_program, 'uMaterial.alpha')
        self.uMaterial_emissiveColor =      glGetUniformLocation(gl_program, 'uMaterial.emissiveColor')

        # Sun uniforms
        self.uSun_ambientColor =            glGetUniformLocation(gl_program, 'uSun.ambientColor')
        self.uSun_diffuseColor =            glGetUniformLocation(gl_program, 'uSun.diffuseColor')
        self.uSun_specularColor =           glGetUniformLocation(gl_program, 'uSun.specularColor')
        self.uSun_lightDirection =          glGetUniformLocation(gl_program, 'uSun.lightDirection')

    def render_model(self, model, opaque, elapsed, camera):
        self.use()

        # Bind matrices
        model.bind_essential_matrices(self, camera)
        glUniformMatrix4fv(self.uTransposeInverseModel, 1, GL_FALSE, model.model.inverse.transpose().tolist())

        # Bind view position
        glUniform3fv(self.uViewPosition, 1, camera.position.tolist())

        # Bind sun
        app.sun.bind_uniforms(self)

        # Bind gamma
        glUniform1f(self.uGamma, app.gamma)

        model.render_meshmtls(opaque, self)
