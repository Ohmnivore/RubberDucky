import math

import glfw
import numpy as np
from pyrr import Vector3, Matrix44

from ducky.app import app
from ducky.camera import Camera

class FlyCamera(Camera):

    def __init__(self):
        super(FlyCamera, self).__init__()
        app.center_mouse()
        self.horizontal_angle = np.pi
        self.vertical_angle = 0.0
        self.movement_multiplier = 75.0
        self.rotation_multiplier = 0.65
        self.rotation_springiness = 75.0
        self.mouse_x = app.mouse_pos[0]
        self.mouse_y = app.mouse_pos[1]

        self.orbiting = False
        self.orbit_distance = 0.0
        self.orbit_anchor = Vector3([0.0, 0.0, 0.0])
        self.orbit_speed = np.pi / 2.0

    def update(self, elapsed):
        super(FlyCamera, self).update(elapsed)

        if app.keys_pressed[glfw.KEY_SPACE]:
            self.orbiting = not self.orbiting
            if self.orbiting:
                diff = (self.position - self.orbit_anchor)
                diff.y = 0.0
                self.orbit_distance = diff.length
                self.horizontal_angle = math.atan2(diff.x, diff.z) - np.pi

        if self.orbiting:
            self.horizontal_angle += elapsed * self.orbit_speed
            cos = math.cos(self.horizontal_angle) * self.orbit_distance
            sin = math.sin(self.horizontal_angle) * self.orbit_distance
            self.position.x = self.orbit_anchor.x - sin
            self.position.z = self.orbit_anchor.z - cos

        if app.mouse_btns[glfw.MOUSE_BUTTON_LEFT] and not self.orbiting:
            # Exponential decay for smoothing
            d = 1.0 - math.exp(math.log(0.5) * self.rotation_springiness * elapsed)
            self.mouse_x += (app.mouse_pos[0] - self.mouse_x) * d
            self.mouse_y += (app.mouse_pos[1] - self.mouse_y) * d

            self.horizontal_angle += self.rotation_multiplier * elapsed * (app.width / 2.0 - self.mouse_x)
            self.vertical_angle   += self.rotation_multiplier * elapsed * (app.height / 2.0 - self.mouse_y)
        app.center_mouse()

        # View matrix
        direction = Vector3([
            math.cos(self.vertical_angle) * math.sin(self.horizontal_angle),
            math.sin(self.vertical_angle),
            math.cos(self.vertical_angle) * math.cos(self.horizontal_angle)
        ])
        right = Vector3([
            math.sin(self.horizontal_angle - np.pi / 2.0),
            0,
            math.cos(self.horizontal_angle - np.pi / 2.0)
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
