from OpenGL.GL import *
from PIL import Image

class Texture:

    def __init__(self, target = GL_TEXTURE_2D):
        self.gl_texture = None
        self.target = target

        self.clamping_s = GL_CLAMP_TO_EDGE
        self.clamping_t = GL_CLAMP_TO_EDGE
        self.clamping_r = GL_CLAMP_TO_EDGE
        self.min_filter = GL_NEAREST
        self.mag_filter = GL_NEAREST

        self.width = 0
        self.height = 0
        self.level = 0

    def create(self):
        self.gl_texture = glGenTextures(1)

    def destroy(self):
        glDeleteTextures(1, self.gl_texture)

    def set_clamping(self, clamping_s, clamping_t, clamping_r):
        self.clamping_s = clamping_s
        self.clamping_t = clamping_t
        self.clamping_r = clamping_r
        glTexParameteri(self.target, GL_TEXTURE_WRAP_S, self.clamping_s)
        glTexParameteri(self.target, GL_TEXTURE_WRAP_T, self.clamping_t)
        glTexParameteri(self.target, GL_TEXTURE_WRAP_R, self.clamping_r)

    def set_filtering(self, min_filter, mag_filter):
        self.min_filter = min_filter
        self.mag_filter = mag_filter
        glTexParameteri(self.target, GL_TEXTURE_MIN_FILTER, self.min_filter)
        glTexParameteri(self.target, GL_TEXTURE_MAG_FILTER, self.mag_filter)

    def generate_mipmaps(self):
        glGenerateMipmap(self.target)

    def bind(self):
        glBindTexture(self.target, self.gl_texture)

    def load_2D(self, pixels, width, height, internal_format = GL_RGB, format = GL_RGB, type = GL_FLOAT, level = 0):
        self.width = width
        self.height = height
        self.level = 0
        glTexImage2D(self.target, self.level, internal_format, self.width, self.height, 0, format, type, pixels)

    def load_2D_from_path(self, path, format, pre_multiply = True, gamma_correct = True, gamma = 0.0):
        with Image.open(path) as image:
            self.load_2D_from_image(image, format, pre_multiply, gamma_correct, gamma)

    def load_2D_from_image(self, image, format, pre_multiply = True, gamma_correct = True, gamma = 0.0):
        # From https://gist.github.com/mozbugbox/10cd35b2872628246140
        if gamma_correct:
            lut = [pow(x / 255.0, gamma) * 255 for x in range(256)]
            lut = lut * 3 # Need one set of data for each band for RGB
            if image.mode == 'RGBA':
                alpha_lut = [x for x in range(256)]
                lut += alpha_lut
            image = image.point(lut)

        # From https://stackoverflow.com/a/31401077
        if pre_multiply:
            transparent = Image.new("RGBA", image.size, (0, 0, 0, 0))
            image = Image.composite(image, transparent, image)

        if format == GL_RGBA:
            width, height, raw = image.size[0], image.size[1], image.tobytes("raw", "RGBA", 0, -1)
        else:
            width, height, raw = image.size[0], image.size[1], image.tobytes("raw", "RGB", 0, -1)
        self.load_2D(raw, width, height, format, format, GL_UNSIGNED_BYTE, 0)
