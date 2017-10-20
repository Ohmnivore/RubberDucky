from OpenGL.GL import *
from OpenGL.GL import shaders

from ducky.app import app
from ducky.state import State
from ducky.model import Model
from ducky.program import Program

from fly_camera import FlyCamera
from outline_model_stencil import OutlineModelStencil

class FlyState(State):

    def __init__(self):
        super(FlyState, self).__init__()

    def create(self):
        super(FlyState, self).create()

        vertex_shader_src = ''
        with open('shaders/default.vert.glsl') as vertex_file:
            vertex_shader_src = vertex_file.read()
        vertex_shader = shaders.compileShader(vertex_shader_src, GL_VERTEX_SHADER)

        fragment_shader_src = ''
        with open('shaders/default.frag.glsl') as fragment_file:
            fragment_shader_src = fragment_file.read()
        fragment_shader = shaders.compileShader(fragment_shader_src, GL_FRAGMENT_SHADER)

        gl_program = shaders.compileProgram(vertex_shader, fragment_shader)
        self.program = Program(gl_program)

        app.camera = FlyCamera()
        app.bg_color.xyz = [0.83, 0.80, 0.75]

        self.car = OutlineModelStencil()
        self.entities.append(self.car)
        self.car.load_obj('assets/car/car.obj')
        self.car.pos += [14.0, 0.0, -28.0]
        self.car.scale.fill(6.0)

        self.girl = OutlineModelStencil()
        self.entities.append(self.girl)
        self.girl.load_obj('assets/low poly girl/low poly girl.obj')
        self.girl.pos += [0.0, 6.0, -24.0]

        # self.teapot = Model()
        # self.entities.append(self.teapot)
        # self.teapot.load_obj('assets/teapot/teapot.obj')
        # self.teapot.pos += [-8.0, 0.0, -24.0]

    def update(self, elapsed):
        super(FlyState, self).update(elapsed)

    def render(self, elapsed, camera):
        super(FlyState, self).render(elapsed, camera, self.program)

    def destroy(self):
        super(FlyState, self).destroy()
