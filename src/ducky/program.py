from OpenGL.GL import *

class Program:

    def __init__(self, gl_program):
        self.gl_program = gl_program

        # MVP
        self.uModel =                       glGetUniformLocation(gl_program, 'uModel')
        self.uTransposeInverseModel =       glGetUniformLocation(gl_program, 'uTransposeInverseModel')
        self.uView =                        glGetUniformLocation(gl_program, 'uView')
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