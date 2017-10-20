import glfw
from OpenGL.GL import *

from ducky.app import app
from ducky.camera import Camera
from ducky.icons import set_icons

def on_key(window, key, scancode, action, mods):
    if action == glfw.PRESS or action == glfw.REPEAT:
        app.keys[key] = True
    elif action == glfw.RELEASE:
        app.keys[key] = False

def on_mouse_btn(window, btn, action, mods):
    if action == glfw.PRESS or action == glfw.REPEAT:
        app.mouse_btns[btn] = True
    elif action == glfw.RELEASE:
        app.mouse_btns[btn] = False

def on_cursor_pos(window, x, y):
    app.mouse_pos.x = x
    app.mouse_pos.y = y

def on_resize(window, width, height):
    app.width = width
    app.height = height
    app.aspect_ratio = app.width / app.height

def start_app(state):
    # Initialize the library
    if not glfw.init():
        return

    # Set 3.3 core profile
    glfw.window_hint(glfw.SAMPLES, app.multisample_bits) # MSAA
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    # Double buffering
    if not app.double_buffer:
        glfw.window_hint(glfw.DOUBLEBUFFER, False)

    # Buffer bits
    glfw.window_hint(glfw.RED_BITS, 8)
    glfw.window_hint(glfw.GREEN_BITS, 8)
    glfw.window_hint(glfw.BLUE_BITS, 8)
    glfw.window_hint(glfw.ALPHA_BITS, 8)
    glfw.window_hint(glfw.DEPTH_BITS, 24)
    glfw.window_hint(glfw.STENCIL_BITS, 8)

    # Create a windowed mode window and its OpenGL context
    monitor = None
    if app.fullscreen:
        monitor = glfw.get_primary_monitor()
        video_mode = glfw.get_video_mode(monitor)
        on_resize(None, video_mode[0][0], video_mode[0][1])
    window = glfw.create_window(app.width, app.height, 'RubberDucky', monitor, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    # Register handlers
    glfw.set_key_callback(window, on_key)
    glfw.set_mouse_button_callback(window, on_mouse_btn)
    glfw.set_cursor_pos_callback(window, on_cursor_pos)
    glfw.set_window_size_callback(window, on_resize)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED) # Disable cursor
    if not app.vsync:
        glfw.swap_interval(0) # Remove v-sync

    # Set window icons
    set_icons(window)

    # Create state and camera
    app.window = window
    app.camera = Camera()
    app.state = state
    app.state.create()

    # Setup OpenGL global config
    if app.multisample_bits > 0:
        glEnable(GL_MULTISAMPLE)
    glEnable(GL_DEPTH_TEST)

    # Timing
    last_frame_time = glfw.get_time()
    time_since_last_render = 0.0

    # Statistics
    last_report_time = last_frame_time
    report_timer = 0.0
    frames_since_last_report = 0
    max_elapsed = 0.0

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        if app.keys[glfw.KEY_ESCAPE]:
            glfw.set_window_should_close(window, True)

        # Timing
        cur_frame_time = glfw.get_time()
        elapsed = cur_frame_time - last_frame_time
        time_since_last_render += elapsed
        last_frame_time = cur_frame_time

        if app.max_fps < 0 or time_since_last_render > 1.0 / app.max_fps:
            # Gathering statistics
            if time_since_last_render > max_elapsed:
                max_elapsed = time_since_last_render
            report_timer += time_since_last_render
            if report_timer > 1.0:
                time_since_last_report = cur_frame_time - last_report_time
                last_report_time = cur_frame_time
                print('FPS: {:.2f}    Max elapsed: {:.4f}'.format(
                    frames_since_last_report / time_since_last_report, max_elapsed))
                report_timer = 0.0
                max_elapsed = 0.0
                frames_since_last_report = 0.0
            frames_since_last_report += 1

            # Clear screen
            glClearColor(app.bg_color[0], app.bg_color[1], app.bg_color[2], 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)

            # Manage state
            app.update(time_since_last_render)
            app.render(time_since_last_render)
            time_since_last_render = 0.0

            # Poll for and process events
            glfw.poll_events()

            # Swap front and back buffers
            if app.double_buffer:
                glfw.swap_buffers(window)
            else:
                glFinish()

    # Shutdown
    state.destroy()
    glfw.terminate()
