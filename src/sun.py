from pyrr import Vector3
from OpenGL.GL import *

class Sun:

    def __init__(self):
        self.ambient_color = Vector3([1.0, 1.0, 1.0])
        self.ambient_strength = 0.1
        self.diffuse_color = Vector3([1.0, 1.0, 1.0])
        self.diffuse_strength = 1.0
        self.specular_color = Vector3([1.0, 1.0, 1.0])
        self.specular_strength = 0.5
        self.light_direction = Vector3([1.0, -1.0, 0.0])

    def bind_uniforms(self, program):
        ambient_color_uni = glGetUniformLocation(program, 'uSun.ambientColor')
        ambient_strength_uni = glGetUniformLocation(program, 'uSun.ambientStrength')
        diffuse_color_uni = glGetUniformLocation(program, 'uSun.diffuseColor')
        diffuse_strength_uni = glGetUniformLocation(program, 'uSun.diffuseStrength')
        specular_color_uni = glGetUniformLocation(program, 'uSun.specularColor')
        specular_strength_uni = glGetUniformLocation(program, 'uSun.specularStrength')
        light_direction_uni = glGetUniformLocation(program, 'uSun.lightDirection')

        glUniform3fv(ambient_color_uni, 1, self.ambient_color.tolist())
        glUniform1f(ambient_strength_uni, self.ambient_strength)
        glUniform3fv(diffuse_color_uni, 1, self.diffuse_color.tolist())
        glUniform1f(diffuse_strength_uni, self.diffuse_strength)
        glUniform3fv(specular_color_uni, 1, self.specular_color.tolist())
        glUniform1f(specular_strength_uni, self.specular_strength)
        glUniform3fv(light_direction_uni, 1, self.light_direction.tolist())
