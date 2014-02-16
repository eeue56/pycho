#!/usr/bin/python2

from __future__ import division

# PyQT4 imports
from PyQt4 import QtGui, QtCore, QtOpenGL
from PyQt4.QtOpenGL import QGLWidget
# PyOpenGL imports
import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo

from random import choice, randint

from pycho.world import World
from pycho.misc import *

from pycho.world_objects import Player, Wall, Bomb, OldGrumper
from pycho.levels import Level, LevelController, generate_objects


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

 
if __name__ == '__main__':
    # import numpy for generating random data points
    import sys
    import logging

    logging.getLogger().setLevel(logging.ERROR)

 
    # define a QT window with an OpenGL widget inside it
    class TestWindow(QtGui.QMainWindow):
        def __init__(self):
            super(TestWindow, self).__init__()
            # initialize the GL widget
            self.player = Player(50, 50, COLOURS['white'], DIRECTIONS['up'], speed=2)

            with open('pycho/level_data.json') as f:
                levels = generate_objects(f.read())

            level_controller = LevelController(levels[0], levels)

            self.world = World(self.player, level_controller)

            self.widget = GLPlotWidget(100, 100, self.world)
            self.keys = set()

            self.widget.setGeometry(0, 0, self.widget.width, self.widget.height)
            self.setCentralWidget(self.widget)
            self.show()

            self.paint_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.paint_timer, QtCore.SIGNAL("timeout()"), self.widget.updateGL)
            self.clean_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.clean_timer, QtCore.SIGNAL("timeout()"), self.world.clean_up)


            QtCore.QMetaObject.connectSlotsByName(self)
            
            self.paint_timer.start(30)
            self.clean_timer.start(500)


            self.resize(600, 400)

        def keyPressEvent(self, event):

            key = event.key()

            if key == QtCore.Qt.Key_A:
                face_movement = DIRECTIONS['left']
            elif key == QtCore.Qt.Key_D:
                face_movement = DIRECTIONS['right']
            elif key == QtCore.Qt.Key_W:
                face_movement = DIRECTIONS['up']
            elif key == QtCore.Qt.Key_S:
                face_movement = DIRECTIONS['down']
            elif key == QtCore.Qt.Key_Space: 
                face_movement = DIRECTIONS['still']
            else:
                return

            self.world.player.facing = face_movement

            self.world.tick()


        def closeEvent(self, event):
            logging.debug("Dumping to text file")
            self.world.mind_dump()
 
    # create the QT App and window
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec_()