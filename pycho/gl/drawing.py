import OpenGL.GL as gl
from numpy import array, float32
from OpenGL.arrays.vbo import VBO

import logging

def draw_square(x, y, x_size=1, y_size=1):
    """ Draw a square of given location and size """
    gl.glRectf(x, y, x + x_size, y + y_size)

def rectangle_coords(x, y, width=1, height=1):
    return [
        [x, y, 0.0],
        [x + width, y, 0.0],
        [x, y + height, 0.0],
        
        [x + width, y + height, 0.0],
        [x, y + height, 0.0],
        [x + width, y, 0.0]
    ]

def color_rectangle_coords(x, y, width=1, height=1, color=(1, 0, 0)):
    r, g, b = color
    return [
        [x, y, 0.0, r, g, b],
        [x + width, y, 0.0, r, g, b],
        [x, y + height, 0.0, r, g, b],
        
        [x + width, y + height, 0.0, r, g, b],
        [x, y + height, 0.0, r, g, b],
        [x + width, y, 0.0, r, g, b]
    ]

def generate_rectangle_vbo(x, y, width=1, height=1):
    return VBO(array(rectangle_coords(x, y, width, height), dtype=float32))

def sections_into_coords(sections):
    out = []

    for (x, y, width, height, color) in sections:
        out.extend(color_rectangle_coords(x, 
            y, 
            width, 
            height, 
            color))

    return out

def sectioned_vbo(sections):
    points = sections_into_coords(sections)
    return (VBO(array(points, dtype=float32)), len(points))

def draw_color_vbo(vbo, offset=0, number=6):
    try:
        vbo.bind()

        try:
            gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
            gl.glEnableClientState(gl.GL_COLOR_ARRAY)

            gl.glVertexPointer(3, gl.GL_FLOAT, 24, vbo)
            gl.glColorPointer(3, gl.GL_FLOAT, 24, vbo + 12)

            gl.glDrawArrays(gl.GL_TRIANGLES, offset, number, None)

        except Exception as e:
            logging.error('failed to draw', e)
        finally:
            vbo.unbind()
            gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
            gl.glDisableClientState(gl.GL_COLOR_ARRAY)
    except Exception as e:
        logging.error('failed to bind', e)
    finally:
        pass

def draw_vbo(vbo, offset=0, number=6):
    try:
        vbo.bind()

        try:
            gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
            gl.glVertexPointerf(vbo)
            gl.glDrawArrays(gl.GL_TRIANGLES, offset, number, None)
        except Exception:
            logging.error('failed to draw')
        finally:
            vbo.unbind()
            gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
    except Exception:
        logging.error('failed to bind')
    finally:
        pass
