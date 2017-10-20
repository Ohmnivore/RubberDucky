from OpenGL.GL import *

from ducky.app import app
from ducky.state import State
from ducky.model import Model
from ducky.default_program import DefaultProgram

from fly_camera import FlyCamera
from outline_stencil_program import OutlineStencilProgram

class FlyState(State):

    def __init__(self):
        super(FlyState, self).__init__()

    def create(self):
        super(FlyState, self).create()
        
        self.default_program = DefaultProgram()
        self.default_program.load_files('shaders/default.vert.glsl', 'shaders/default.frag.glsl')

        self.outline_program = OutlineStencilProgram(self.default_program)
        self.outline_program.load_files('shaders/outline_stencil.vert.glsl', 'shaders/outline_stencil.frag.glsl')

        app.camera = FlyCamera()
        app.bg_color.xyz = [0.83, 0.80, 0.75]

        self.car = Model()
        self.entities.append(self.car)
        self.car.load_obj('assets/car/car.obj')
        self.car.pos += [14.0, 0.0, -28.0]
        self.car.scale.fill(6.0)

        self.girl = Model()
        self.entities.append(self.girl)
        self.girl.load_obj('assets/low poly girl/low poly girl.obj')
        self.girl.pos += [0.0, 6.0, -24.0]

        # self.teapot = Model()
        # self.entities.append(self.teapot)
        # self.teapot.load_obj('assets/teapot/teapot.obj')
        # self.teapot.pos += [-8.0, 0.0, -24.0]

    def update(self, elapsed):
        super(FlyState, self).update(elapsed)

    def pre_render(self, elapsed):
        super(FlyState, self).pre_render(elapsed)

    def render(self, elapsed, camera):
        # Opaque render pass first, then transparent
        for entity in self.entities:
            self.outline_program.render_model(entity, True, elapsed, camera)

        glDepthMask(GL_FALSE)
        glEnable(GL_CULL_FACE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        for entity in self.entities:
            self.outline_program.render_model(entity, False, elapsed, camera)

        glDepthMask(GL_TRUE)
        glDisable(GL_CULL_FACE)
        glDisable(GL_BLEND)

    def destroy(self):
        super(FlyState, self).destroy()
        self.default_program.destroy()
        self.outline_program.destroy()
