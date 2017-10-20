import glfw
import numpy as np
from PIL import Image

def set_icons(window):
    sizes = np.array(['32'])
    icons = []
    for size in sizes:
        filepath = 'assets/icons/' + size + '.png'

        with Image.open(filepath) as image:
            image_arr = np.fromstring(image.tobytes(), dtype=np.uint8)
            image_arr = image_arr.reshape((image.size[1], image.size[0], 4))
            icons.append((image.width, image.height, image_arr))

    glfw.set_window_icon(window, len(sizes), icons[0]) # Only setting one for now because of library limitation
