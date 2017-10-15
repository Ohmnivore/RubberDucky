from state import State
from model import Model
from OpenGL.GL import *
from OpenGL.GL import shaders
from pyrr import Vector3, Matrix44
from app import app
import glfw
import math

class FlyState(State):

    def __init__(self):
        vertex_shader_src = ''
        with open('shaders/vertex.glsl') as vertex_file:
            vertex_shader_src = vertex_file.read()
        vertex_shader = shaders.compileShader(vertex_shader_src, GL_VERTEX_SHADER)

        fragment_shader_src = ''
        with open('shaders/fragment.glsl') as fragment_file:
            fragment_shader_src = fragment_file.read()
        fragment_shader = shaders.compileShader(fragment_shader_src, GL_FRAGMENT_SHADER)

        self.shader = shaders.compileProgram(vertex_shader, fragment_shader)

        self.char = Model()
        self.char.loadObj('assets/low poly girl/low poly girl.obj')
        # self.char.loadObj('assets/triangle/triangle.obj')
        # self.char.loadObj('assets/teapot/teapot.obj')

        self.cam_pos = Vector3([0, 0, 0])
        self.heading = 0

    def update(self):
        if app.keys[glfw.KEY_ESCAPE]:
            exit()
            return

        mov = [0, 0, 0]
        if app.keys[glfw.KEY_A]:
            mov = [-0.1, 0, 0]
        elif app.keys[glfw.KEY_D]:
            mov = [0.1, 0, 0]
        if app.keys[glfw.KEY_W]:
            mov = [0, 0, 0.1]
        elif app.keys[glfw.KEY_S]:
            mov = [0, 0, -0.1]
        if app.keys[glfw.KEY_Q]:
            mov = [0, 0.1, 0]
        elif app.keys[glfw.KEY_E]:
            mov = [0, -0.1, 0]
        
        self.cam_pos = self.cam_pos + mov

        if app.keys[glfw.KEY_LEFT]:
            self.heading += 0.01
        elif app.keys[glfw.KEY_RIGHT]:
            self.heading -= 0.01

        self.char.update()

    def render(self):
        # View matrix
        view = Matrix44.look_at(
            self.cam_pos,
            self.cam_pos - Vector3([math.cos(self.heading), 0, math.sin(self.heading)]),
            Vector3([0, 1, 0]))

        # Projection matrix
        projection = Matrix44.perspective_projection(app.fov, app.aspect_ratio, app.near, app.far)

        glUseProgram(self.shader)
        self.char.render(self.shader, view, projection)
        glUseProgram(0)

    def destroy(self):
        self.char.destroy()
