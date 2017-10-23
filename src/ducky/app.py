import glfw
import numpy as np
from pyrr import Vector3

from ducky.sun import Sun
from ducky.texture import create_default_texture

class App:

    def __init__(self):
        self.fullscreen = False
        self.width = 1280
        self.height = 720
        self.max_fps = -1.0
        self.fov = 45.0
        self.near = 0.1
        self.far = 1000.0
        self.gamma = 2.2
        self.bg_color = Vector3([1.0, 1.0, 1.0])
        self.multisample_bits = 8
        self.double_buffer = True
        self.vsync = False
        self.force_flat_shading = False

        # Aspect ratio
        self.aspect_ratio = self.width / self.height

        # Mouse input
        self.mouse_pos = Vector3([0.0, 0.0, 0.0])
        self.mouse_btns = np.full(glfw.MOUSE_BUTTON_LAST, False)
        self.mouse_btns_pressed = np.full(glfw.MOUSE_BUTTON_LAST, False)
        self.mouse_btns_released = np.full(glfw.MOUSE_BUTTON_LAST, False)

        # Keyboard input
        self.keys = np.full(glfw.KEY_LAST, False)
        self.keys_pressed = np.full(glfw.KEY_LAST, False)
        self.keys_released = np.full(glfw.KEY_LAST, False)

        # Global lighting
        self.sun = Sun()
        self.sun.gamma_correct(self.gamma)

        self.window = None # Set by start_app()
        self.camera = None # A default camera is created by start_app()
        self.state = None  # Set by start_app()

    def create(self, window, camera, state):
        create_default_texture()
        app.window = window
        app.camera = camera
        app.state = state
        app.state.create()

    def update(self, elapsed):
        self.camera.update(elapsed)
        self.state.update(elapsed)
        self.mouse_btns_pressed.fill(False)
        self.mouse_btns_released.fill(False)
        self.keys_pressed.fill(False)
        self.keys_released.fill(False)

    def render(self, elapsed):
        self.camera.pre_render(elapsed)
        self.state.pre_render(elapsed)
        self.state.render(elapsed, self.camera)

    def set_mouse_pos(self, x, y):
        glfw.set_cursor_pos(self.window, x, y)
        self.mouse_pos[0] = x
        self.mouse_pos[1] = y

    def center_mouse(self):
        self.set_mouse_pos(self.width / 2, self.height / 2)

app = App()
