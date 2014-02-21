from __future__ import division

from pycho.world_objects import WorldObject
from pycho.world.navigation import DIRECTIONS

from pycho.gl.color import COLORS

try:
    xrange(1)
except NameError:
    xrange = range

class Wall(WorldObject):
    def __init__(self, 
        x, 
        y, 
        width=5, 
        gaps=None, 
        color=COLORS['grey'], 
        facing=DIRECTIONS['up'], 
        speed=0,
        *args,
        **kwargs):
        WorldObject.__init__(self, x, y, color, facing, damagable=False, moveable=False, *args, **kwargs)

        if gaps is None:
            gaps = []

        self.gaps = gaps
        self.speed = speed
        self.width = width
        self.height = 2
        self.health = 1

    def tick(self, world):
        pass

    def take_damage(self, damage, world):
        pass

    def populated_at(self, *args):
        populated = []
        populate = lambda x, y: populated.append((x, y, self.color))
        x, y = self.x, self.y

        if self.facing == DIRECTIONS['down']:
            for i in xrange(x):
                if i not in self.gaps:
                    for w in xrange(self.width):
                        populate(i, w)
        elif self.facing == DIRECTIONS['up']:
            for i in xrange(x):
                if i not in self.gaps:
                    for w in xrange(y - self.width, y):
                        populate(i, w)
        elif self.facing == DIRECTIONS['left']:
            for j in xrange(y):
                if j not in self.gaps:
                    for w in xrange(self.width):
                        populate(w, j)
        elif self.facing == DIRECTIONS['right']:
            for j in xrange(y):
                if j not in self.gaps:
                    for w in xrange(x - self.width, x):
                        populate(w, j)

        return populated