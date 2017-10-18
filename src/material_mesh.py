from pyrr import Vector3
import array
from OpenGL.GL import *

class Material:

    def __init__(self):
        self.ambient_color = Vector3([0.0, 0.0, 0.0])
        self.diffuse_color = Vector3([0.0, 0.0, 0.0])
        self.specular_color = Vector3([0.0, 0.0, 0.0])
        self.specular_exponent = 0.0
        self.alpha = 0.0
    
    def bind_uniforms(self, program):
        ambient_uni = glGetUniformLocation(program, 'uMaterial.ambientColor')
        diffuse_uni = glGetUniformLocation(program, 'uMaterial.diffuseColor')
        specular_uni = glGetUniformLocation(program, 'uMaterial.specularColor')
        specular_exponent_uni = glGetUniformLocation(program, 'uMaterial.specularExponent')
        alpha_uni = glGetUniformLocation(program, 'uMaterial.alpha')

        glUniform3fv(ambient_uni, 1, self.ambient_color.tolist())
        glUniform3fv(diffuse_uni, 1, self.diffuse_color.tolist())
        glUniform3fv(specular_uni, 1, self.specular_color.tolist())
        glUniform1f(specular_exponent_uni, self.specular_exponent)
        glUniform1f(alpha_uni, self.alpha)

    def destroy(self):
        pass

class Face:

    def __init__(self):
        self.vertices = []
        self.texcoords = []
        self.normals = []

class Mesh:

    def __init__(self):
        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []
        self.vbo = None
        self.vao = None
    
    def gen_buffers(self):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        flat_list = []

        faceIdx = 0
        for face in self.faces:
            for i in range(0, 3):
                idx = faceIdx * 3 + i
                vertex = self.vertices[face.vertices[i]]
                texcoords = [0.0, 0.0]
                if len(face.texcoords) > i:
                    texcoords = self.texcoords[face.texcoords[i]]
                normal = [0.0, 0.0, 1.0]
                if len(face.normals) > i:
                    normal = self.normals[face.normals[i]]
                
                flat_list.append(vertex[0])
                flat_list.append(vertex[1])
                flat_list.append(vertex[2])
                flat_list.append(texcoords[0])
                flat_list.append(texcoords[1])
                flat_list.append(normal[0])
                flat_list.append(normal[1])
                flat_list.append(normal[2])

            faceIdx += 1
        
        self.vbo = self.gen_buffer(flat_list)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(0 * 4))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(5 * 4))
        glEnableVertexAttribArray(2)

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)
    
    def gen_buffer(self, flat_list):
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)

        arr = array.array('f', flat_list)
        glBufferData(GL_ARRAY_BUFFER, len(flat_list) * 4, arr.tostring(), GL_STATIC_DRAW)
        return buffer

    def destroy(self):
        glDeleteVertexArrays(1, [self.vao])
        glDeleteBuffers(1, [self.vbo])

class MaterialMesh:

    def __init__(self):
        self.mtl = Material()
        self.mesh = Mesh()

    def render(self, program):
        self.mtl.bind_uniforms(program)
        glBindVertexArray(self.mesh.vao)
        glDrawArrays(GL_TRIANGLES, 0, len(self.mesh.faces) * 3)

    def destroy(self):
        self.mesh.destroy()
        self.mtl.destroy()
