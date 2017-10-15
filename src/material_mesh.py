import numpy

class Material:

    def __init__(self):
        self.ambient = numpy.array([0, 0, 0])
        self.diffuse = numpy.array([0, 0, 0])
        self.specular = numpy.array([0, 0, 0])
        self.specularExponent = 0.0
        self.transparency = 0.0

class MaterialMesh:

    def __init__(self):
        self.mtl = Material()
