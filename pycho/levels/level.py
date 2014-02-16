from pycho.world_exceptions import *

try:
    xrange(2)
except NameError:
    xrange = range


class Level(object):

    def __init__(self, color, walls, width, height, objects=None):
        self.color = color
        self.walls = walls
        self.width = width
        self.height = height

        if objects is None:
            objects = []

        self.objects = []

        self.object_array = [[None for x in xrange(width)] for y in xrange(height)]

        self.add_objects(objects)

    def _clean_remains(self, populated):
        for (x, y) in populated:
            self.object_array[y][x] = None

    def add_object(self, object_):
        populated = []
        for (x, y, _) in object_.populated_squares:
            try:
                self.object_array[y][x] = object_
            except IndexError:
                self._clean_remains(populated)
                raise OutOfWorldException

            populated.append((x, y))
        self.objects.append(object_)

    def add_objects(self, objects):
        for object_ in objects:
            self.add_object(object_)

