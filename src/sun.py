from pyrr import Vector3
from OpenGL.GL import *
from math_util import pow_vec_3D

class Sun:

    def __init__(self):
        self.ambient_color = Vector3([1.0, 1.0, 1.0])
        self.ambient_strength = 0.3
        self.diffuse_color = Vector3([1.0, 1.0, 1.0])
        self.diffuse_strength = 1.0
        self.specular_color = Vector3([1.0, 1.0, 1.0])
        self.specular_strength = 0.3
        self.light_direction = Vector3([1.0, -1.0, -0.5])

    def bind_uniforms(self, program):
        glUniform3fv(program.uSun_ambientColor, 1,      (self.ambient_color * self.ambient_strength).tolist())
        glUniform3fv(program.uSun_diffuseColor, 1,      (self.diffuse_color * self.diffuse_strength).tolist())
        glUniform3fv(program.uSun_specularColor, 1,     (self.specular_color * self.specular_strength).tolist())
        glUniform3fv(program.uSun_lightDirection, 1,    self.light_direction.tolist())

    def gamma_correct(self, gamma):
        pow_vec_3D(self.ambient_color, gamma)
        pow_vec_3D(self.diffuse_color, gamma)
        pow_vec_3D(self.specular_color, gamma)
