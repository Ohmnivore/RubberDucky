from pyrr import Vector3, Matrix44, Quaternion
import os.path as path
from obj_parser import MtlParser, ObjParser
from OpenGL.GL import *

class Model:

    def __init__(self):
        self.pos = Vector3([0.0, 0.0, 0.0])
        self.scale = Vector3([1.0, 1.0, 1.0])
        self.rot = Vector3([0.0, 0.0, 0.0])
        self.orientation = Quaternion()
        self.meshmtl_map = None

    def load_obj(self, filepath):
        # Reading source files
        obj_path = filepath
        mtl_path = path.splitext(filepath)[0] + '.mtl'

        mtl_parser = MtlParser()
        with open(mtl_path) as mtl_file:
            mtl_parser.parse_string(mtl_file.read())
        
        obj_parser = ObjParser()
        with open(obj_path) as obj_file:
            obj_parser.parse_string(mtl_parser.mtl_map, obj_file.read())
        
        self.meshmtl_map = obj_parser.mtl_map
        
        # Uploading to GPU
        for name, meshmtl in self.meshmtl_map.items():
            meshmtl.mesh.gen_buffers()
    
    def update(self, elapsed):
        pass

    def render(self, elapsed, camera, program):
        # Model matrix
        model = Matrix44.from_scale(self.scale)
        model = model * self.orientation
        translation = Matrix44.from_translation(self.pos)
        model = model * translation

        # MVP matrix
        mvp = camera.projection * camera.view * model
        mvpUni = glGetUniformLocation(program, 'mvp')
        glUniformMatrix4fv(mvpUni, 1, GL_FALSE, mvp.tolist())

        for name, meshmtl in self.meshmtl_map.items():
            meshmtl.render(program)
    
    def destroy(self):
        for name, meshmtl in self.meshmtl_map.items():
            meshmtl.destroy()
