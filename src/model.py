import numpy
import os.path as path
from obj_parser import MtlParser

class Model:

    def __init__(self):
        self.pos = numpy.array([0, 0, 0])
        self.scale = numpy.array([0, 0, 0])
        self.rot = numpy.array([0, 0, 0])

    def loadObj(self, filepath):
        obj_path = filepath
        mtl_path = path.splitext(filepath)[0] + '.mtl'

        mtl_parser = MtlParser()
        with open(mtl_path) as mtl_file:
            mtl_parser.parseString(mtl_file.read())
    
    def render(self):
        pass
