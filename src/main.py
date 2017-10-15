import glfw
from OpenGL.GL import *
from app import app
from camera import Camera
from fly_state import FlyState
import time

def on_key(window, key, scancode, action, mods):
    if action == glfw.PRESS or action == glfw.REPEAT:
        app.keys[key] = True
    elif action == glfw.RELEASE:
        app.keys[key] = False

def on_resize(window, width, height):
    app.width = width
    app.height = height
    app.aspect_ratio = app.width / app.height

def main():
    # Initialize the library
    if not glfw.init():
        return

    # Set 3.3 core profile
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.DOUBLEBUFFER, False)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(app.width, app.height, 'RubberDucky', None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    # Register handlers
    glfw.set_window_size_callback(window, on_resize)
    glfw.set_key_callback(window, on_key)
    glfw.swap_interval(0)

    # Create state and camera
    camera = Camera()
    state = FlyState()

    # Setup OpenGL global config
    glClearColor(1, 1, 1, 1)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)

    # Timing
    last_frame = time.time()
    report_timer = 0
    max_elapsed = 0

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        if app.keys[glfw.KEY_ESCAPE]:
            glfw.set_window_should_close(window, True)

        # Timing
        cur_frame = time.time()
        elapsed = cur_frame - last_frame
        if elapsed > max_elapsed:
            max_elapsed = elapsed
        last_frame = cur_frame
        report_timer += elapsed
        if report_timer > 1:
            print('FPS: {} Max elapsed: {}'.format(int(1.0 / elapsed), max_elapsed))
            report_timer = 0
            max_elapsed = 0

        if elapsed > 0:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Manage state and camera
            camera.update(elapsed)
            state.update(elapsed)
            state.render(elapsed, camera)

            # Poll for and process events
            glfw.poll_events()

            # Swap front and back buffers
            glfw.swap_buffers(window)
            glFinish()

    # Shutdown
    state.destroy()
    glfw.terminate()

if __name__ == '__main__':
    main()
