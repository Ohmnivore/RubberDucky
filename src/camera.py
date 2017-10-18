from pyrr import Vector3, Matrix44
import math
import glfw
from app import app
import numpy

class Camera:

    def __init__(self):
        self.position = Vector3([0.0, 0.0, 0.0])
        self.horizontal_angle = numpy.pi
        self.vertical_angle = 0.0
        self.view = Matrix44.identity()
        self.projection = Matrix44.identity()
        self.movement_multiplier = 75.0
        self.rotation_multiplier = 75.0

    def update(self, elapsed):
        if app.keys[glfw.KEY_LEFT]:
            self.horizontal_angle += 0.01 * self.rotation_multiplier * elapsed
        elif app.keys[glfw.KEY_RIGHT]:
            self.horizontal_angle -= 0.01 * self.rotation_multiplier * elapsed
        if app.keys[glfw.KEY_UP]:
            self.vertical_angle += 0.01 * self.rotation_multiplier * elapsed
        elif app.keys[glfw.KEY_DOWN]:
            self.vertical_angle -= 0.01 * self.rotation_multiplier * elapsed

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

        # Projection matrix
        self.projection = Matrix44.perspective_projection(app.fov, app.aspect_ratio, app.near, app.far)
