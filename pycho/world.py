from __future__ import division, print_function

from pycho.world_exceptions import *
from pycho.misc import *

from pycho.world_objects import Word, Wall
from pycho.hivemind import Action

from random import choice

try:
    xrange(1)
except NameError:
    xrange = range

class World(object):

    def __init__(self, player, level_controller):
        self.player = player

        self.level_controller = level_controller
        self.level_controller.start()

    def add_object(self, *args, **kwargs):
        """ Adds an object to the current level """
        self.level_controller.current_level.add_object(*args, **kwargs)

    @property
    def floor_color(self):
        return self.level_controller.current_level.color

    @property
    def height(self):
        return self.level_controller.current_level.height

    @property
    def width(self):
        return self.level_controller.current_level.width

    @property
    def object_array(self):
        return self.level_controller.current_level.object_array

    @property
    def objects(self):
        return self.level_controller.current_level.objects

    @property
    def current_level(self):
        return self.level_controller.current_level

    def remove(self, object_):
        """ Removes the object from the world - but not the level """
        #TODO: remove from level as well
        for (x, y, _) in object_.populated_squares:
            self.object_array[y][x] = None
        self.objects.remove(object_)

    def _move(self, old, new, object_):
        """ Moves the object from old to new """
        for (x, y, _) in old:
            self.object_array[y][x] = None
        for (new_x, new_y, _) in new:
            self.object_array[new_y][new_x] = object_

    def _move_object(self, object_, x=0, y=0):
        """ Moves the object by x and y """
        self._move(object_.populated_squares, 
            object_.populated_at(object_.x + x, object_.y + y), 
            object_)
        object_.x += x
        object_.y += y

    def colliding_object(self, old_object, populated_next):
        """ Returns the colliding object using the next populated 
            squares or None if none exists. If the object moves 
            out of the world (or level), then OutOfWorldException 
            is raised
        """
        for (x, y, _) in populated_next:
            if y < 0 or y >= self.height or x < 0 or x >= self.width:
                raise OutOfWorldException

            if self.object_array[y][x] is not None and self.object_array[y][x] != old_object:
                return self.object_array[y][x]
        return None

    def direction_to_object(self, object_to_move, object_to_meet):
        """ Returns the direction the object should face in 
            order to move towards the object desired to meet 
        """
        x, y = object_to_move.x, object_to_move.y
        i, j = object_to_meet.x, object_to_meet.y

        direction = DIRECTIONS['still']

        if j < y:
            direction += DIRECTIONS['down']
        elif j > y:
            direction += DIRECTIONS['up']

        if i < x:
            direction += DIRECTIONS['left']
        elif i > x:
            direction += DIRECTIONS['right']

        return direction

    def object_going_to_collide(self, object_, x=0, y=0):
        """ Works out if the object is going to collide when it moves
            by x, y
        """
        projected_points = object_.populated_at(object_.x + x, object_.y + y)
        return self.colliding_object(object_, projected_points)

    def move_in_direction(self, object_, direction, distance=1):
        """ Attempts to move the object in direction and distance
            Throws CollisionException is collides, OutOfWorldException 
            if the object_ moves out of the world 
        """
        x, y = MOVEMENTS[direction]
            
        for _ in xrange(distance):
            obj_ = self.object_going_to_collide(object_, x=x, y=y)

            if obj_ is not None:
                raise CollisionException(obj_)
                
            self._move_object(object_, x=x, y=y)

    def next_level(self):
        """ Moves to next level based on the way the player 
            is facing """
        self.level_controller.next_level(self.player.facing)

    def clean_up(self):
        """ Cleans up the objects in the world """
        copy = [[None for x in xrange(self.width)] for y in xrange(self.height)]

        for object_ in self.objects:
            for (x, y, _) in object_.populated_squares:
                copy[y][x] = object_

        self.level_controller.current_level.object_array = copy

    def is_near_player(self, object_, distance_x=50, distance_y=50, debug=False):
        """ Works out if the object is near the player 
            Used as a render clip 
        """
        return True
        return (object_.x - distance_x < self.player.x < object_.x + distance_x \
            and object_.y - distance_y < self.player.y < object_.y + distance_y)

    def draw(self):
        """ Draws objects in the world """
        for object_ in self.objects:
            if isinstance(object_, Word):
                object_._debug_draw()
            else:
                if isinstance(object_, Wall):
                    object_.draw()
                else:
                    if self.is_near_player(object_):
                        object_.draw()

        self.player.draw()

    def _move_player_into_gap(self, direction):
        """ Places the player in the door way of the level """
        for object_ in self.objects:
            if isinstance(object_, Wall) and object_.facing == direction:
                if direction in [DIRECTIONS['right'], DIRECTIONS['left']]:
                    self.player.y = int((object_.gaps[0] + object_.gaps[-1]) / 2)

                    if object_.facing == DIRECTIONS['right']:
                        self.player.x = self.width - (object_.width + 10)
                    else:
                        self.player.x = (object_.width + 2)

                else:
                    self.player.x = int((object_.gaps[0] + object_.gaps[-1]) / 2)

                    if object_.facing == DIRECTIONS['up']:
                        self.player.y = self.height - (object_.width + 10)
                    else:
                        self.player.y = (object_.width + 2)


    @Action('Moved to new level')
    def _move_to_next_level(self):
        """ Moves the world to the next level """
        self.next_level()
        self.clean_up()

        direction = opposite_direction(self.player.facing)
        self._move_player_into_gap(direction)

        

    def tick(self):
        """ Does a tick of the world """
        #TODO: use time-based deltatimes
        for object_ in self.objects:
            object_.tick(self)

        try:
            self.player.tick(self)
        except OutOfWorldException:
            self._move_to_next_level()
                    
        for object_ in self.objects:
            if object_.health <= 0:
                object_.die()
                self.remove(object_)


        ## TODO: kill player
        if self.player.health <= 0:
            self.add_object(Word(20, 20, "you died", color=(1, 0, 0)))
            print("Game over, you died!")
            

    def mind_dump(self):
        """ Dump the mind of all the objects """
        for object_ in self.objects:
            object_.mind.dump(repr(object_))

        self.player.mind.dump(repr(self.player))