from __future__ import division

from PyQt5 import QtCore, QtWidgets

from pycho.gui.widgets import GLPlotWidget
from pycho.world.navigation import DIRECTIONS

from pycho.gui.interaction import KEYS

from pycho.world.helpers import box_around

import logging

xrange = range

class DefaultWindow(QtWidgets.QMainWindow):
    def __init__(self, game, 
        key_press_handler=None, 
        mouse_click_handler=None,
        mouse_release_handler=None):
        super(DefaultWindow, self).__init__()

        self.game = game
        
        self.widget = GLPlotWidget(100, 100, self.game)
        self.keys = set()

        self.widget.setGeometry(0, 0, self.widget.width, self.widget.height)
        self.setCentralWidget(self.widget)
        self.show()

        self.paint_timer = QtCore.QBasicTimer()

        self.clean_timer = QtCore.QBasicTimer()

        self.callbacks = [self.widget.updateGL, self.game.world.clean_up]
        QtCore.QMetaObject.connectSlotsByName(self)
        
        self.paint_timer.start(30, self)
        self.clean_timer.start(40, self)

        self.resize(600, 400)


        if key_press_handler is None:
            key_press_handler = lambda self, event: self._defaultKeyPressHandler(event)

        if mouse_click_handler is None:
            mouse_click_handler = lambda self, event: self._defaultMousePressHandler(event)

        if mouse_release_handler is None:
            mouse_release_handler = lambda *a, **kw: None

        self.key_press_handler = key_press_handler
        self.mouse_click_handler = mouse_click_handler
        self.mouse_release_handler = mouse_release_handler

    def timerEvent(self, event):
        self.callbacks[event.timerId() - 1]()

    def _defaultKeyPressHandler(self, event):
        key = event.key()

        if key == KEYS['A']:
            face_movement = DIRECTIONS['left']
        elif key == KEYS['D']:
            face_movement = DIRECTIONS['right']
        elif key == KEYS['W']:
            face_movement = DIRECTIONS['up']
        elif key == KEYS['S']:
            face_movement = DIRECTIONS['down']
        elif key == KEYS['Space']: 
            face_movement = DIRECTIONS['still']
        else:
            return

        self.game.player.facing = face_movement
        self.game.world.tick()

    def map_point_to_game_world(self, x, y):
        i = int((x / self.widget.width) * self.game.world.width)
        j = int(((self.widget.height - y) / self.widget.height) * self.game.world.height)
        return (i, j)

    def _defaultMousePressHandler(self, event, pointer_size=5):
        x, y = self.map_point_to_game_world(event.x(), event.y())

        logging.error(x)
        logging.error(y)

        for j in xrange(pointer_size):
            try:
                obj = self.game.world.colliding_object(None, 
                    box_around(x, y, j, j))
            except:
                break

            if obj is not None:
                logging.error(obj)
                break
        else:
            logging.error("Nothing found!")

    def keyPressEvent(self, event):
        self.key_press_handler(self, event)

    def mousePressEvent(self, event):
        self.mouse_click_handler(self, event)

    def mouseReleaseEvent(self, event):
        self.mouse_release_handler(self, event)

    def closeEvent(self, event):
        logging.debug("Dumping to text file")
        self.game.world.mind_dump()
