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

    def load_uniform_locations(self, gl_program):
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
