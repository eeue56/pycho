from __future__ import division

from pycho.world_objects import WorldObject, Bomb
from pycho.world_exceptions import *

from pycho.hivemind import Action

try:
    xrange(1)
except NameError:
    xrange = range

class Player(WorldObject):
    def __init__(self, 
        x, 
        y, 
        color, 
        facing, 
        health=3, 
        scale=1, 
        speed=1,
        *args, 
        **kwargs):
        WorldObject.__init__(self, x, y, color, facing, health=3, scale=scale, *args, **kwargs)
        self.speed = speed

    def populated_at(self, x, y):
        """ returns a list of tuples containing the coordinates of populated 
            squares, should the square be at this point
        """

        #   ###
        #  #####
        #    #
        #-> ###
        #  01234
        populated = []
        populate = lambda x, y, color: populated.append((x, y, color))

        scaled_x = 5 * self.scale
        scaled_y = 4 * self.scale

        ## TODO: fix y scaling

        # bottom and top lines
        for i in xrange(x + 1, x + scaled_x - 1):
            populate(i, y, self.color)
            populate(i, y + scaled_y - 1, self.color)

        # connector

        middle_x = x + int(scaled_x / 2)
        populate(middle_x, y + 1, (1, 0, 0))

        # arms

        for i in xrange(x, x + scaled_x):
            populate(i, y + 2, self.color)

        return populated

    def tick(self, world):
        try:
            self.move(world, self.facing, self.speed)
        except CollisionException as e:
            self.take_damage(5, e.other)
            e.other.take_damage(0.05, self)
        except OutOfWorldException:
            raise

    def take_damage(self, damage, other):
        WorldObject.take_damage(self, damage, other)

        