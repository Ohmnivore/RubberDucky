from pyrr import Vector3, Matrix44
from ducky.app import app

class Camera:

    def __init__(self):
        self.position = Vector3([0.0, 0.0, 0.0])
        self.view = Matrix44.identity()
        self.projection = Matrix44.identity()

    def update(self, elapsed):
        # Projection matrix
        self.projection = Matrix44.perspective_projection(app.fov, app.aspect_ratio, app.near, app.far)
