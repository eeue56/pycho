import OpenGL.GL as gl

def draw_square(x, y, x_size=1, y_size=1):
    """ Draw a square of given location and size """
    gl.glRectf(x, y, x + x_size, y + y_size)

def generate_rectangle_vbo_vertex(x, y, width=1, height=1):
    return [
        x, y, 0.0,
        x + width, y, 0.0,
        x, y + height, 0.0,
        
        x + width, y + height, 0.0,
        x, y + height, 0.0,
        x + width, y, 0.0
    ]