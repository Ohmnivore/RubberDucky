from OpenGL.GL import *

from ducky.app import app
from ducky.state import State
from ducky.model import Model
from ducky.default_program import DefaultProgram

from fly_camera import FlyCamera
from outline_wireframe_program import OutlineWireframeProgram
from outline_wireframe_constant_pixel_program import OutlineWireframeConstantPixelProgram
from outline_scale_program import OutlineScaleProgram
from outline_scale_constant_program import OutlineScaleConstantProgram
from outline_scale_constant_pixel_program import OutlineScaleConstantPixelProgram
from outline_derivatives_program import OutlineDerivativesProgram

class FlyState(State):

    def __init__(self):
        super(FlyState, self).__init__()

    def create(self):
        super(FlyState, self).create()
        
        self.default_program = DefaultProgram()
        self.default_program.load_files('shaders/default.vert.glsl', 'shaders/default.frag.glsl')

        # self.outline_program = OutlineWireframeProgram(self.default_program, 1.0)
        # self.outline_program.load_files('shaders/outline_wireframe.vert.glsl', 'shaders/outline_wireframe.frag.glsl')

        self.outline_program = OutlineWireframeConstantPixelProgram(self.default_program, 1.0)
        self.outline_program.load_files('shaders/outline_wireframe_constant_pixel.vert.glsl', 'shaders/outline_wireframe_constant_pixel.frag.glsl')

        # self.outline_program = OutlineScaleProgram(self.default_program, 0.1)
        # self.outline_program.load_files('shaders/outline_scale.vert.glsl', 'shaders/outline_scale.frag.glsl')

        # self.outline_program = OutlineScaleConstantProgram(self.default_program, 1.0, True)
        # self.outline_program.load_files('shaders/outline_scale_constant.vert.glsl', 'shaders/outline_scale_constant.frag.glsl')

        # self.outline_program = OutlineScaleConstantPixelProgram(self.default_program, 1.0)
        # self.outline_program.load_files('shaders/outline_scale_constant_pixel.vert.glsl', 'shaders/outline_scale_constant_pixel.frag.glsl')

        # self.outline_program = OutlineDerivativesProgram()
        # self.outline_program.load_files('shaders/outline_derivatives.vert.glsl', 'shaders/outline_derivatives.frag.glsl')

        self.program = self.outline_program

        app.camera = FlyCamera()
        app.camera.position.xyz = [0.0, 6, 0.0]
        app.bg_color.xyz = [0.83, 0.80, 0.75]

        self.car = Model()
        self.entities.append(self.car)
        self.car.load_obj('assets/car/car.obj')
        self.car.pos.xyz = [4.0, 0.0, -32.0]
        self.car.scale.fill(6.0)

        self.girl = Model()
        self.entities.append(self.girl)
        self.girl.load_obj('assets/low poly girl/low poly girl.obj')
        self.girl.pos.xyz = [-10.0, 6.0, -28.0]

        # self.teapot = Model()
        # self.entities.append(self.teapot)
        # self.teapot.load_obj('assets/teapot/teapot.obj')
        # self.teapot.pos.xyz = [-8.0, 0.0, -24.0]

        app.camera.orbit_anchor.xyz = self.girl.pos

    def update(self, elapsed):
        super(FlyState, self).update(elapsed)

    def pre_render(self, elapsed):
        super(FlyState, self).pre_render(elapsed)

    def render(self, elapsed, camera):
        # Opaque render pass first, then transparent
        for entity in self.entities:
            self.program.render_model(entity, True, elapsed, camera)

        glDepthMask(GL_FALSE)
        glEnable(GL_CULL_FACE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        for entity in self.entities:
            self.program.render_model(entity, False, elapsed, camera)

        glDepthMask(GL_TRUE)
        glDisable(GL_CULL_FACE)
        glDisable(GL_BLEND)

    def destroy(self):
        super(FlyState, self).destroy()
        self.default_program.destroy()
        self.outline_program.destroy()
