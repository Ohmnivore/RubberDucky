from pyrr import Vector3, Matrix44, Quaternion
import os.path as path
from obj_parser import MtlParser, ObjParser
from OpenGL.GL import *
from app import app

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
            meshmtl.mtl.gamma_correct(app.gamma)
            meshmtl.mesh.gen_buffers()
    
    def update(self, elapsed):
        pass

    def render(self, opaque, elapsed, camera, program):
        # Model matrix
        model = Matrix44.from_scale(self.scale)
        model = model * self.orientation
        translation = Matrix44.from_translation(self.pos)
        model = model * translation

        # MVP matrix
        model_uni = glGetUniformLocation(program, 'uModel')
        view_uni = glGetUniformLocation(program, 'uView')
        projection_uni = glGetUniformLocation(program, 'uProjection')
        glUniformMatrix4fv(model_uni, 1, GL_FALSE, model.tolist())
        glUniformMatrix4fv(view_uni, 1, GL_FALSE, camera.view.tolist())
        glUniformMatrix4fv(projection_uni, 1, GL_FALSE, camera.projection.tolist())

        # View position
        view_position_uni = glGetUniformLocation(program, 'uViewPosition')
        glUniform3fv(view_position_uni, 1, camera.position.tolist())

        # Sun
        app.sun.bind_uniforms(program)

        # Gamma
        gamma_uni = glGetUniformLocation(program, 'uGamma')
        glUniform1f(gamma_uni, app.gamma)

        for name, meshmtl in self.meshmtl_map.items():
            if opaque and meshmtl.mtl.alpha == 1.0:
                meshmtl.render(program)
            elif not opaque and meshmtl.mtl.alpha < 1.0:
                meshmtl.render(program)
    
    def destroy(self):
        for name, meshmtl in self.meshmtl_map.items():
            meshmtl.destroy()
