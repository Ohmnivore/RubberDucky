import numpy
import array
from OpenGL.GL import *

class Material:

    def __init__(self):
        self.ambient = numpy.array([0, 0, 0])
        self.diffuse = numpy.array([0, 0, 0])
        self.specular = numpy.array([0, 0, 0])
        self.specularExponent = 0.0
        self.transparency = 0.0

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
    
    def genBuffers(self):
        flat_list = []

        faceIdx = 0
        for face in self.faces:
            for i in range(0, 3):
                idx = faceIdx * 3 + i
                vertex = self.vertices[face.vertices[i]]
                texcoords = [0, 0]
                if len(face.texcoords) > i:
                    texcoords = self.texcoords[face.texcoords[i]]
                normal = [0, 0, 1]
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
        
        self.vbo = self.genBuffer(flat_list)
    
    def genBuffer(self, flat_list):
        buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buffer)

        arr = array.array('f', flat_list)
        glBufferData(GL_ARRAY_BUFFER, len(arr) * arr.itemsize, arr.tostring(), GL_STATIC_DRAW)
        return buffer

class MaterialMesh:

    def __init__(self):
        self.mtl = Material()
        self.mesh = Mesh()
