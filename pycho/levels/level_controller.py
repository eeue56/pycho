from pycho.levels.level_exceptions import *

class LevelController(object):

    def __init__(self, levels, first=None):

        self.current_level = None
        self.levels = levels

        if first is None:
            for level in levels.values():
                if level.is_first:
                    first = level
                    break

        self.current_level = first

    def start(self):
        pass

    def next_level(self, direction):
        if self.current_level is None:
            raise NoCurrentLevelException

        if direction not in self.current_level.walls:
            raise NoSuchLevelException

        self.current_level = self.levels[self.current_level.walls[direction]]