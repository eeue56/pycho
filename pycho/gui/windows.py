from PyQt4 import QtGui, QtCore, QtOpenGL

from pycho.gui.widgets import GLPlotWidget
from pycho.misc import *

class DefaultWindow(QtGui.QMainWindow):
    def __init__(self, game):
        super(DefaultWindow, self).__init__()

        self.game = game
        
        self.widget = GLPlotWidget(100, 100, self.game)
        self.keys = set()

        self.widget.setGeometry(0, 0, self.widget.width, self.widget.height)
        self.setCentralWidget(self.widget)
        self.show()

        self.paint_timer = QtCore.QTimer()
        QtCore.QObject.connect(self.paint_timer, QtCore.SIGNAL("timeout()"), self.widget.updateGL)
        self.clean_timer = QtCore.QTimer()
        QtCore.QObject.connect(self.clean_timer, QtCore.SIGNAL("timeout()"), self.game.world.clean_up)

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

        self.game.player.facing = face_movement

        self.game.world.tick()


    def closeEvent(self, event):
        logging.debug("Dumping to text file")
        self.world.mind_dump()
