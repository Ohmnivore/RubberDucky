from OpenGL.GL import *
from PIL import Image
from pyrr import Vector4

class Texture:

    def __init__(self, target = GL_TEXTURE_2D):
        self.gl_texture = None
        self.created = False
        self.target = target
        self.mipmaps_generated = False

        self.clamping_s = GL_CLAMP_TO_EDGE
        self.clamping_t = GL_CLAMP_TO_EDGE
        self.clamping_r = GL_CLAMP_TO_EDGE
        self.border_color = Vector4([0.0, 0.0, 0.0, 0.0])
        self.min_filter = GL_NEAREST
        self.mag_filter = GL_NEAREST

        self.width = 0
        self.height = 0
        self.internal_format = None
        self.format = None
        self.type = None
        self.level = 0

    def create(self):
        self.gl_texture = glGenTextures(1)
        self.created = True

    def destroy(self):
        if self.created:
            glDeleteTextures(self.gl_texture)
            self.created = False

    def set_clamping(self, clamping_s, clamping_t, clamping_r):
        self.clamping_s = clamping_s
        self.clamping_t = clamping_t
        self.clamping_r = clamping_r
        glTexParameteri(self.target, GL_TEXTURE_WRAP_S, clamping_s)
        glTexParameteri(self.target, GL_TEXTURE_WRAP_T, clamping_t)
        glTexParameteri(self.target, GL_TEXTURE_WRAP_R, clamping_r)

    def set_border_color(self, border_color):
        self.border_color = border_color
        glTexParameterfv(self.target, GL_TEXTURE_BORDER_COLOR, border_color.astype('float32').tobytes());  

    def set_filtering(self, min_filter, mag_filter):
        self.min_filter = min_filter
        self.mag_filter = mag_filter
        glTexParameteri(self.target, GL_TEXTURE_MIN_FILTER, min_filter)
        glTexParameteri(self.target, GL_TEXTURE_MAG_FILTER, mag_filter)

    def generate_mipmaps(self):
        self.mipmaps_generated = True
        glGenerateMipmap(self.target)

    def bind(self):
        glBindTexture(self.target, self.gl_texture)

    def load_2D(self, pixels, width, height, internal_format = GL_RGB, format = GL_RGB, type = GL_FLOAT, level = 0):
        self.width = width
        self.height = height
        self.internal_format = internal_format
        self.format = format
        self.type = type
        self.level = 0
        glTexImage2D(self.target, level, internal_format, width, height, 0, format, type, pixels)

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


transparent_pixel_texture = Texture()

def create_default_textures():
    global transparent_pixel_texture
    transparent_pixel_texture.create()
    transparent_pixel_texture.bind()
    transparent_pixel_texture.set_filtering(GL_NEAREST, GL_NEAREST)
    transparent_pixel_texture.set_clamping(GL_REPEAT, GL_REPEAT, GL_REPEAT)
    white = Image.new("RGBA", (2, 2), (0, 0, 0, 0))
    transparent_pixel_texture.load_2D(white.tobytes("raw", "RGBA", 0, -1), 2, 2, GL_RGBA, GL_RGBA, GL_UNSIGNED_BYTE, 0)

def destroy_default_textures():
    global transparent_pixel_texture
    transparent_pixel_texture.destroy()
