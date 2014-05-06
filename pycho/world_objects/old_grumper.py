from __future__ import division

from pycho.world_objects import WorldObject, Bomb
from pycho.world.world_exceptions import *

from pycho.hivemind import Action

from random import randint, choice

try:
    xrange(1)
except NameError:
    xrange = range


class OldGrumper(WorldObject):
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

    def populated_at(self, x, y):
        """ returns a list of tuples containing the coordinates of populated 
            squares, should the square be at this point
        """

        #   #
        #  ###
        #   #
        #-># #
        #  01234
        populated = []
        populate = lambda i, j, color: populated.append((x + i, y + j, color))

        scaled_x = 5 * self.scale
        scaled_y = 4 * self.scale

        middle_x = int(scaled_x / 2)
        middle_y = int(scaled_y / 2)

        ## TODO: fix y scaling

        # bottom and top lines
        for i in xrange(scaled_x):
            populate(i, 0, self.color)

            populate(i, scaled_y - 2, (0.5, 1, 0))

        # connector

        populate(middle_x, 1, (1, 0, 0))
        populate(middle_x, scaled_y - 1, (1, 0, 0))
        

        return populated

    def take_damage(self, damage, other):
        if other is self:
            return
        WorldObject.take_damage(self, damage, other)

    def deal_damage(self, other):
        other.take_damage(0.1, self)

    @Action('move away from player', type='defence')
    def move_away_from_player(self, world):
        try:
            direction = world.direction_to_object(self, world.player)
            # jitter
            if randint(0, 100) < 10:
                direction = DIRECTIONS[choice(DIRECTIONS.keys())]

            self.facing = opposite_direction(direction)
            self.move(world, self.facing, 1)
        except CollisionException as e:
            e.other.take_damage(other, self)
        except OutOfWorldException:
            pass

    @Action('stay still', type='defence')
    def stay_still(self, world):
        self.facing = DIRECTIONS['still']

    @Action('move towards player', type='attack')
    def move_towards_player(self, world):
        try:
            self.facing = world.direction_to_object(self, world.player)
            self.move(world, self.facing, 1)
        except CollisionException as e:
            e.other.take_damage(5, self)
        except OutOfWorldException:
            pass
        

    def tick(self, world):
        behavior = choice(['attack', 'attack', 'attack', 'attack' 'defence'])
        self.mind.next_move(behavior)(world)