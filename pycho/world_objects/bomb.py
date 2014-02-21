from __future__ import division

from pycho.world_objects import WorldObject
from pycho.world.navigation import DIRECTIONS, opposite_direction
from pycho.world_exceptions import *

from pycho.gl.color import COLORS

from random import randint, choice

possibles = [x for x in DIRECTIONS.keys() if x != 'still']

try:
    xrange(1)
except NameError:
    xrange = range

class Fragment(WorldObject):
    def __init__(self, x, y, 
        color=COLORS['grey'], 
        facing=DIRECTIONS['up'], 
        health=3, 
        scale=1,
        max_scale=3, 
        speed=2,
        spawner=None,
        *args, 
        **kwargs):

        WorldObject.__init__(self, x, y, color, facing, health=health, scale=scale, spawner=spawner, *args, **kwargs)


        self.speed = speed

    def tick(self, world):
        self.health -= 0.02

        try:
            self.move(world, self.facing, self.speed)
        except CollisionException as e:
            e.other.take_damage((3 - self.health) * 2, self)
            self.health = 0
        except OutOfWorldException:
            self.health = 0
 

class Bomb(WorldObject):
    def __init__(self, x, y, 
        color=COLORS['grey'], 
        facing=DIRECTIONS['up'], 
        health=3, 
        scale=1,
        max_scale=3,
        spawner=None,
        *args, 
        **kwargs):

        WorldObject.__init__(self, x, y, color, facing, health=health, scale=scale, spawner=spawner, *args, **kwargs)
        self.center_color = COLORS['red']
        self.max_scale = max_scale

    def populated_at(self, x, y):
        """ returns a list of tuples containing the coordinates of populated 
            squares, should the square be at this point
        """

        #  ###   2
        #  #n#   1
        #->###   0
        #
        #  012
        populated = []
        populate = lambda i, j, color: populated.append((i + x, j + y, color))

        scaled_x = int(3 * self.scale)
        scaled_y = int(3 * self.scale)


        for i in xrange(1, scaled_x - 1):
            for j in xrange(1, scaled_y - 1):
                populate(i, j, self.center_color)

        for i in xrange(scaled_x):
            populate(i, 0, self.color)
            populate(i, scaled_y - 1, self.color)

        
        for j in xrange(scaled_y):
            populate(0, j, (0, 1, 0))
            populate(scaled_x - 1, j, self.color)
        

        return populated

    def tick(self, world):
        
        if self.scale < self.max_scale:
            self.scale += 0.1
        else:
            self.health -= 0.25

            if self.health < 1:
                for x in xrange(randint(10, 15)):

                    direction = DIRECTIONS[choice(possibles)]
                    fragment = Fragment(self.x + randint(-10, 10), self.y + randint(-10, 10), facing=direction)
                    world.add_object(fragment)
                self.scale += 1

        try:
            self.move(world, self.facing)
        except CollisionException as e:

            if self.health < 1:
                e.other.take_damage(3 - self.health, self)

            self.scale -= 0.2
            try:
                self.facing = opposite_direction(self.facing)
                self.move(world, self.facing)
            except CollisionException:
                self.scale -= 0.5
                self.max_scale = self.scale
                
        except OutOfWorldException:
            self.health = 0