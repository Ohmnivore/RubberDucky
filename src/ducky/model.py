import os.path as path

from OpenGL.GL import *
from pyrr import Vector3, Matrix44, Quaternion

from ducky.app import app
from ducky.obj_parser import MtlParser, ObjParser

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
            meshmtl.mesh.gen_buffers(app.force_flat_shading)
    
    def update(self, elapsed):
        pass

    def render(self, opaque, elapsed, camera, program):
        glUseProgram(program.gl_program)

        # Model matrix
        model = Matrix44.from_scale(self.scale)
        translation = Matrix44.from_translation(self.pos)
        model = translation * self.orientation * model

        # MVP matrix
        glUniformMatrix4fv(program.uModel, 1, GL_FALSE, model.tolist())
        glUniformMatrix4fv(program.uTransposeInverseModel, 1, GL_FALSE, model.inverse.transpose().tolist())
        glUniformMatrix4fv(program.uView, 1, GL_FALSE, camera.view.tolist())
        glUniformMatrix4fv(program.uProjectionView, 1, GL_FALSE, (camera.projection * camera.view).tolist())

        # View position
        glUniform3fv(program.uViewPosition, 1, camera.position.tolist())

        # Sun
        app.sun.bind_uniforms(program)

        # Gamma
        glUniform1f(program.uGamma, app.gamma)

        for name, meshmtl in self.meshmtl_map.items():
            if opaque and meshmtl.mtl.alpha == 1.0:
                meshmtl.render(program)
            elif not opaque and meshmtl.mtl.alpha < 1.0:
                meshmtl.render(program)
    
    def destroy(self):
        for name, meshmtl in self.meshmtl_map.items():
            meshmtl.destroy()
