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

        # Textures
        self.uTexAmbient =                  glGetUniformLocation(gl_program, 'uTexAmbient')
        self.uTexDiffuse =                  glGetUniformLocation(gl_program, 'uTexDiffuse')
        self.uTexSpecular =                 glGetUniformLocation(gl_program, 'uTexSpecular')
        self.uTexEmissive =                 glGetUniformLocation(gl_program, 'uTexEmissive')

        # Sun uniforms
        self.uSun_ambientColor =            glGetUniformLocation(gl_program, 'uSun.ambientColor')
        self.uSun_diffuseColor =            glGetUniformLocation(gl_program, 'uSun.diffuseColor')
        self.uSun_specularColor =           glGetUniformLocation(gl_program, 'uSun.specularColor')
        self.uSun_lightDirection =          glGetUniformLocation(gl_program, 'uSun.lightDirection')

    def render_model(self, model, opaque, elapsed, camera):
        self.use()

        # Bind matrices
        glUniformMatrix4fv(self.uModel, 1, GL_FALSE, model.model.astype('float32').tobytes())
        glUniformMatrix4fv(self.uProjectionView, 1, GL_FALSE, camera.projection_view.astype('float32').tobytes())
        model_view = camera.view * model.model
        glUniformMatrix4fv(self.uTransposeInverseModel, 1, GL_FALSE, model_view.inverse.transpose().astype('float32').tobytes())

        # Bind view position
        glUniform3fv(self.uViewPosition, 1, camera.position.astype('float32').tobytes())

        # Bind sun
        app.sun.bind_uniforms(self)

        # Bind gamma
        glUniform1f(self.uGamma, app.gamma)

        self.render_meshmtls(self.render_meshmtl, model, opaque)

    def render_meshmtls(self, cb_func, model, opaque):
        for name, meshmtl in model.meshmtl_map.items():
            if opaque and meshmtl.mtl.alpha == 1.0:
                cb_func(meshmtl)
            elif not opaque and meshmtl.mtl.alpha < 1.0:
                cb_func(meshmtl)

    def render_meshmtl(self, meshmtl):
        meshmtl.mtl.bind_uniforms(self)
        glBindVertexArray(meshmtl.mesh.vao)
        glDrawArrays(GL_TRIANGLES, 0, len(meshmtl.mesh.faces) * 3)
