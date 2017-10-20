import glfw
from pyrr import Vector3

from ducky.sun import Sun

class App:

    def __init__(self):
        self.window = None # Set by start_app()

        self.fullscreen = False
        self.width = 1280
        self.height = 720
        self.max_fps = -1.0
        self.fov = 45.0
        self.near = 0.1
        self.far = 1000.0
        self.gamma = 2.2
        self.bg_color = Vector3([1.0, 1.0, 1.0])
        self.force_flat_shading = True
        self.camera = None # A default camera is created by start_app()

        # Aspect ratio
        self.aspect_ratio = self.width / self.height

        # Mouse input
        self.mouse_pos = Vector3([0.0, 0.0, 0.0])
        self.mouse_btns = []
        for btn in range(0, 12):
            self.mouse_btns.append(False)

        # Keyboard input
        self.keys = []
        for key in range(0, 360):
            self.keys.append(False)

        # Global lighting
        self.sun = Sun()
        self.sun.gamma_correct(self.gamma)

    def set_mouse_pos(self, x, y):
        glfw.set_cursor_pos(self.window, x, y)
        self.mouse_pos[0] = x
        self.mouse_pos[1] = y

    def center_mouse(self):
        self.set_mouse_pos(self.width / 2, self.height / 2)

app = App()
