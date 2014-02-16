from PyQt4.QtOpenGL import QGLWidget

import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo

class GLPlotWidget(QGLWidget):

    def __init__(self, width, height, world, *args):
        QGLWidget.__init__(self, *args)
        self.width = width
        self.height = height
        self.world = world
        self.last_level = world.current_level
 
    def initializeGL(self):
        """Initialize OpenGL, VBOs, upload data on the GPU, etc.
        """
        # background color
        gl.glClearColor(0,0,0,0)
        gl.glViewport(0, 0, self.width, self.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

    def paintGL(self):
        """Paint the scene.
        """
        # clear the buffer

        if self.last_level != self.world.current_level:
            self.last_level = self.world.current_level
            self.resizeGL(self.width, self.height)

        r, g, b = self.world.floor_color
        gl.glClearColor(r, g, b, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

        self.world.draw()
        
    def resizeGL(self, width, height):
        """Called upon window resizing: reinitialize the viewport.
        """
        # update the window size    
        self.width, self.height = width, height
        # paint within the whole window
        gl.glViewport(0, 0, self.width, self.height)
        # set orthographic projection (2D only)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        # the window corner OpenGL coordinates are the same as the world height and width
        gl.glOrtho(0, self.world.width, 0, self.world.height, -1, 1)
