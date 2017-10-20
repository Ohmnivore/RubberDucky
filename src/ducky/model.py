import os.path as path

from pyrr import Vector3, Matrix44, Quaternion

from ducky.app import app
from ducky.obj_parser import MtlParser, ObjParser

class Model:

    def __init__(self):
        self.pos = Vector3([0.0, 0.0, 0.0])
        self.scale = Vector3([1.0, 1.0, 1.0])
        self.rot = Vector3([0.0, 0.0, 0.0])
        self.orientation = Quaternion()
        self.model = Matrix44.identity()
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
            meshmtl.mtl.gamma_correct(app.gamma)
            meshmtl.mesh.gen_buffers(app.force_flat_shading)
    
    def update(self, elapsed):
        pass

    def pre_render(self, elapsed):
        # Model matrix
        self.model = Matrix44.from_scale(self.scale)
        translation = Matrix44.from_translation(self.pos)
        self.model = translation * self.orientation * self.model
    
    def destroy(self):
        for name, meshmtl in self.meshmtl_map.items():
            meshmtl.destroy()
