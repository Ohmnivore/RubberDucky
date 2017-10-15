from pyrr import Vector3, Matrix44, Quaternion
import os.path as path
from obj_parser import MtlParser, ObjParser
from OpenGL.GL import *

class Model:

    def __init__(self):
        self.pos = Vector3([0, 0, 0])
        self.scale = Vector3([1, 1, 1])
        self.rot = Vector3([0, 0, 0])
        self.orientation = Quaternion()
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
    
    def update(self):
        pass

    def render(self, program, view, projection):
        # Model matrix
        model = Matrix44.from_scale(self.scale)
        model = model * self.orientation
        translation = Matrix44.from_translation(self.pos)
        model = model * translation
        # model = Matrix44.identity()

        # MVP matrix
        mvp = projection * view * model
        mvpUni = glGetUniformLocation(program, 'mvp')
        glUniformMatrix4fv(mvpUni, 1, GL_FALSE, mvp.tolist())

        for name, meshmtl in self.meshmtl_map.items():
            meshmtl.render()
    
    def destroy(self):
        for name, meshmtl in self.meshmtl_map.items():
            meshmtl.destroy()
