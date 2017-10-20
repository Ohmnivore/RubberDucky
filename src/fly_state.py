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
        
        self.program = Program()
        self.program.load_files('shaders/default.vert.glsl', 'shaders/default.frag.glsl')

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
