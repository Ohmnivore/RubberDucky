from sun import Sun

class App:

    def __init__(self):
        self.fullscreen = False
        self.width = 1080
        self.height = 720
        self.max_fps = -1.0
        self.fov = 45.0
        self.near = 0.1
        self.far = 1000.0

        self.aspect_ratio = self.width / self.height
        self.keys = []
        for key in range(0, 360):
            self.keys.append(False)
        self.sun = Sun()

app = App()
