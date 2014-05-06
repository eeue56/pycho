from pycho.world.world_exceptions import *

from pycho.levels.helpers import color_tuple_to_dict
from json import dumps

try:
    xrange(1)
except NameError:
    xrange = range

class Level(object):

    def __init__(self, 
        color, 
        walls, 
        width, 
        height, 
        level_id=None,
        objects=None, 
        is_first=None):
        self.color = color
        self.walls = walls
        self.width = width
        self.height = height

        if objects is None:
            objects = []

        self.objects = []

        self.object_array = [[None for x in xrange(width)] for y in xrange(height)]

        self.add_objects(objects)

        if is_first is None:
            is_first = False

        if level_id is None:
            level_id = '*'

        self.id = level_id
        self.is_first = is_first

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

    def to_json(self):

        return dumps({
            'is_first' : self.is_first,
            'width' : self.width,
            'height' : self.height,
            'color' : color_tuple_to_dict(self.color),
        })