import array

from OpenGL.GL import *
from pyrr import Vector3

from ducky.math_util import pow_vec_3D

class Material:

    def __init__(self):
        self.diffuse_texture = None
        self.ambient_color = Vector3([0.0, 0.0, 0.0])
        self.diffuse_color = Vector3([0.0, 0.0, 0.0])
        self.specular_color = Vector3([0.0, 0.0, 0.0])
        self.specular_exponent = 0.0
        self.emissive_color = Vector3([0.0, 0.0, 0.0])
        self.alpha = 0.0
    
    def bind_uniforms(self, program):
        glUniform3fv(program.uMaterial_ambientColor, 1,     self.ambient_color.astype('float32').tobytes())
        glUniform3fv(program.uMaterial_diffuseColor, 1,     self.diffuse_color.astype('float32').tobytes())
        glUniform3fv(program.uMaterial_specularColor, 1,    self.specular_color.astype('float32').tobytes())
        glUniform1f(program.uMaterial_specularExponent,     self.specular_exponent)
        glUniform3fv(program.uMaterial_emissiveColor, 1,    self.emissive_color.astype('float32').tobytes())
        glUniform1f(program.uMaterial_alpha,                self.alpha)
        if self.diffuse_texture != None:
            glActiveTexture(GL_TEXTURE0)
            self.diffuse_texture.bind()
            glUniform1i(program.uTexDiffuse, 0)

    def gamma_correct(self, gamma):
        pow_vec_3D(self.ambient_color, gamma)
        pow_vec_3D(self.diffuse_color, gamma)
        pow_vec_3D(self.specular_color, gamma)
        pow_vec_3D(self.emissive_color, gamma)

    def destroy(self):
        if self.diffuse_texture != None:
            self.diffuse_texture.destroy()

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
    
    def gen_buffers(self, force_flat_shading):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        flat_list = []

        faceIdx = 0
        for face in self.faces:
            # Generate normal from vertices if doesn't exist
            # Gives it flat shading: all three vertices have the face's normal
            normal = [0.0, 0.0, 0.0]
            if force_flat_shading or len(face.normals) == 0:
                p0 = self.vertices[face.vertices[0]]
                p1 = self.vertices[face.vertices[1]]
                p2 = self.vertices[face.vertices[2]]
                u = [p1[0] - p0[0], p1[1] - p0[1], p1[2] - p0[2]]
                v = [p2[0] - p0[0], p2[1] - p0[1], p2[2] - p0[2]]
                normal[0] = u[1] * v[2] - u[2] * v[1]
                normal[1] = u[2] * v[0] - u[0] * v[2]
                normal[2] = u[0] * v[1] - u[1] * v[0]

            for i in range(0, 3):
                idx = faceIdx * 3 + i
                vertex = self.vertices[face.vertices[i]]
                texcoords = [0.0, 0.0]
                if len(face.texcoords) > i:
                    texcoords = self.texcoords[face.texcoords[i]]
                if not force_flat_shading and len(face.normals) > i:
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

    def destroy(self):
        self.mesh.destroy()
        self.mtl.destroy()
