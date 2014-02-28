import OpenGL.GL as gl
from numpy import array, float32
from OpenGL.arrays.vbo import VBO

import logging

def draw_square(x, y, x_size=1, y_size=1):
    """ Draw a square of given location and size """
    gl.glRectf(x, y, x + x_size, y + y_size)

def generate_rectangle_vbo(x, y, width=1, height=1):
    return VBO(array([
        [x, y, 0.0],
        [x + width, y, 0.0],
        [x, y + height, 0.0],
        
        [x + width, y + height, 0.0],
        [x, y + height, 0.0],
        [x + width, y, 0.0]
    ], dtype=float32))

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
