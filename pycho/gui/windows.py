from __future__ import division

from PyQt5 import QtCore, QtWidgets

from pycho.gui.widgets import GLPlotWidget
from pycho.world.navigation import DIRECTIONS

from pycho.gui.interaction import QT_KEYS, is_left, is_right, is_up, is_down

from pycho.world.helpers import box_around

import logging

xrange = range
TURN_BASED = 0

#Qt uses camelCase for naming methods, 
#hence why they are used here

class DefaultWindow(QtWidgets.QMainWindow):
    def __init__(self, game, 
        key_press_handler=None, 
        mouse_click_handler=None,
        mouse_release_handler=None,
        tick_time=0,
        width=600,
        height=400,
        key_press_handlers=None,
        mouse_click_handlers=None,
        mouse_release_handlers=None):
        super(DefaultWindow, self).__init__()

        self.game = game
        
        self.widget = GLPlotWidget(100, 100, self.game)

        self.widget.setGeometry(0, 0, self.widget.width, self.widget.height)
        self.setCentralWidget(self.widget)
        self.show()

        self.paint_timer = QtCore.QBasicTimer()
        self.clean_timer = QtCore.QBasicTimer()

        self.tick_timer = QtCore.QBasicTimer()

        self.callbacks = [self.widget.updateGL, self.game.world.clean_up, self.game.world.tick]
        QtCore.QMetaObject.connectSlotsByName(self)
        
        self.paint_timer.start(30, self)
        self.clean_timer.start(40, self)

        self.timers = [self.paint_timer, self.clean_timer]
        self.timer_times = [30, 40]

        if tick_time != TURN_BASED:
            self.tick_timer.start(tick_time, self)

            self.timers.append(self.tick_timer)
            self.timer_times.append(tick_time)

        self.resize(width, height)


        if key_press_handler is None:
            key_press_handler = lambda self, event: self._defaultKeyPressHandler(event)

        if mouse_click_handler is None:
            mouse_click_handler = lambda self, event: self._defaultMousePressHandler(event)

        if mouse_release_handler is None:
            mouse_release_handler = lambda *a, **kw: None
    
        if key_press_handlers is None:
            key_press_handlers = {'*' : key_press_handler}

        if mouse_click_handlers is None:
            mouse_click_handlers = {'*' : mouse_click_handler}

        if mouse_release_handlers is None:
            mouse_release_handlers = {'*' : mouse_release_handler}

        self.key_press_handlers = key_press_handlers
        self.mouse_click_handlers = mouse_click_handlers
        self.mouse_release_handlers = mouse_release_handlers

        self.is_paused = False

    def timerEvent(self, event):
        self.callbacks[event.timerId() - 1]()

    def _defaultKeyPressHandler(self, event):
        key = event.key()

        logging.debug('Key {} was pressed'.format(key))

        if is_left(key):
            face_movement = DIRECTIONS['left']
        elif is_right(key):
            face_movement = DIRECTIONS['right']
        elif is_up(key):
            face_movement = DIRECTIONS['up']
        elif is_down(key):
            face_movement = DIRECTIONS['down']
        elif key == QT_KEYS['Space']: 
            face_movement = DIRECTIONS['still']
        else:
            return

        logging.debug('Face movement set to {}'.format(face_movement))
        logging.debug('Player is facing {}'.format(self.game.player.facing))

        self.game.player.facing = face_movement
        self.game.world.tick()

    def map_point_to_game_world(self, x, y):
        i = int((x / self.widget.width) * self.game.world.width)
        j = int(((self.widget.height - y) / self.widget.height) * self.game.world.height)
        return (i, j)

    def _current_handler(self, handlers):
        level_id = self.game.world.current_level.id

        if level_id not in handlers:
            try:
                return handlers['*']
            except KeyError:
                logging.error('No default handler set as *!')

        return handlers[level_id]

    def _defaultMousePressHandler(self, event, pointer_size=5):
        x, y = self.map_point_to_game_world(event.x(), event.y())

        # gradually grow the pointer to be bigger to 
        # allow for a greater control on what is clicked
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

    def pause(self):
        for timer in self.timers:
            self.timers.stop()
        self.is_paused = True

    def unpause(self):
        for timer, time in zip(self.timers, self.timer_times):
            self.timers.start(time)
        self.is_paused = False

    def keyPressEvent(self, event):
        self._current_handler(self.key_press_handlers)(self, event)

    def mousePressEvent(self, event):
        self._current_handler(self.mouse_click_handlers)(self, event)

    def mouseReleaseEvent(self, event):
        self._current_handler(self.mouse_release_handlers)(self, event)

    def closeEvent(self, event):
        logging.debug("Dumping to text file")
        self.game.world.mind_dump()
