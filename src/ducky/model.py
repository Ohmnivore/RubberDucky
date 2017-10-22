from os import path

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
        obj_parser = ObjParser(path.dirname(filepath))
        with open(filepath) as obj_file:
            obj_parser.parse_string(obj_file.read())
        
        self.meshmtl_map = obj_parser.mtl_map
        
        # Uploading to GPU
        for name, meshmtl in self.meshmtl_map.items():
            meshmtl.mtl.gamma_correct(app.gamma)
            meshmtl.mesh.gen_buffers(app.force_flat_shading)
    
    def update(self, elapsed):
        pass

    def pre_render(self, elapsed):
        self.compute_model_matrix(elapsed)

    def compute_model_matrix(self, elapsed):
        self.model = Matrix44.from_scale(self.scale)
        self.model = self.model * self.orientation
        translation = Matrix44.from_translation(self.pos)
        self.model = translation * self.model
    
    def destroy(self):
        for name, meshmtl in self.meshmtl_map.items():
            meshmtl.destroy()
