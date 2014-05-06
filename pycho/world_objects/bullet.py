from __future__ import division

from pycho.world_objects import WorldObject
from pycho.world.navigation import DIRECTIONS
from pycho.world.world_exceptions import *

from pycho.gl.color import COLORS

from random import randint, choice


class Bullet(WorldObject):
    def __init__(self, x, y, 
        color=COLORS['grey'], 
        facing=DIRECTIONS['up'], 
        health=1, 
        scale=1,
        max_scale=3,
        spawner=None,
        *args, 
        **kwargs):

        WorldObject.__init__(self, x, y, color, facing, health=health, scale=scale, spawner=spawner, *args, **kwargs)

    def tick(self, world):
        try:
            self.move(world, self.facing)
        except CollisionException as e:
            e.other.take_damage(1, self)
            self.take_damage(1, e.other)