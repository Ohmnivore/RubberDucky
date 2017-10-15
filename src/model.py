import numpy
import os.path as path
from obj_parser import MtlParser, ObjParser

class Model:

    def __init__(self):
        self.pos = numpy.array([0, 0, 0])
        self.scale = numpy.array([0, 0, 0])
        self.rot = numpy.array([0, 0, 0])
        self.meshmtl_map = None

    def loadObj(self, filepath):
        # Reading source files
        obj_path = filepath
        mtl_path = path.splitext(filepath)[0] + '.mtl'

        mtl_parser = MtlParser()
        with open(mtl_path) as mtl_file:
            mtl_parser.parseString(mtl_file.read())
        
        obj_parser = ObjParser()
        with open(obj_path) as obj_file:
            obj_parser.parseString(mtl_parser.mtl_map, obj_file.read())
        
        self.meshmtl_map = obj_parser.mtl_map
        
        # Uploading to GPU
        for name, meshmtl in self.meshmtl_map.items():
            meshmtl.mesh.genBuffers()
    
    def render(self):
        for name, meshmtl in self.meshmtl_map.items():
            meshmtl.render()
