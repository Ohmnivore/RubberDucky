from pyrr import Vector3, Matrix44
from camera import Camera
from app import app
import glfw
import math
import numpy

class FlyCamera(Camera):

    def __init__(self):
        super(FlyCamera, self).__init__()
        app.center_mouse()
        self.horizontal_angle = numpy.pi
        self.vertical_angle = 0.0
        self.movement_multiplier = 75.0
        self.rotation_multiplier = 0.65
        self.rotation_springiness = 75.0
        self.mouse_x = app.mouse_pos[0]
        self.mouse_y = app.mouse_pos[1]

    def update(self, elapsed):
        super(FlyCamera, self).update(elapsed)

        if app.mouse_btns[glfw.MOUSE_BUTTON_LEFT]:
            # Exponential decay for smoothing
            d = 1.0 - math.exp(math.log(0.5) * self.rotation_springiness * elapsed)
            self.mouse_x += (app.mouse_pos[0] - self.mouse_x) * d
            self.mouse_y += (app.mouse_pos[1] - self.mouse_y) * d
            delta = [app.width / 2.0 - self.mouse_x, app.height / 2.0 - self.mouse_y]

            self.horizontal_angle += self.rotation_multiplier * elapsed * delta[0]
            self.vertical_angle   += self.rotation_multiplier * elapsed * delta[1]
        app.center_mouse()

        # View matrix
        direction = Vector3([
            math.cos(self.vertical_angle) * math.sin(self.horizontal_angle),
            math.sin(self.vertical_angle),
            math.cos(self.vertical_angle) * math.cos(self.horizontal_angle)
        ])
        right = Vector3([
            math.sin(self.horizontal_angle - numpy.pi / 2.0),
            0,
            math.cos(self.horizontal_angle - numpy.pi / 2.0)
        ])
        up = Vector3.cross( right, direction )

        if app.mouse_btns[glfw.MOUSE_BUTTON_LEFT]:
            if app.keys[glfw.KEY_A]:
                self.position -= right * self.movement_multiplier * elapsed
            elif app.keys[glfw.KEY_D]:
                self.position += right * self.movement_multiplier * elapsed
            if app.keys[glfw.KEY_W]:
                self.position += direction * self.movement_multiplier * elapsed
            elif app.keys[glfw.KEY_S]:
                self.position -= direction * self.movement_multiplier * elapsed
            if app.keys[glfw.KEY_Q]:
                self.position += up * self.movement_multiplier * elapsed
            elif app.keys[glfw.KEY_E]:
                self.position -= up * self.movement_multiplier * elapsed

        self.view = Matrix44.look_at(
            self.position,
            self.position + direction,
            up
        )
