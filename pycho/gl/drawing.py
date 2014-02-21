import OpenGL.GL as gl

def draw_square(x, y, x_size=1, y_size=1):
    """ Draw a square of given location and size """
    gl.glRectf(x, y, x + x_size, y + y_size)