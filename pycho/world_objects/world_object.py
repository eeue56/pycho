from __future__ import division

import OpenGL.GL as gl

from pycho.gl.drawing import draw_square

from pycho.core.blocking import into_sections


from pycho.world.navigation import DIRECTIONS

from pycho.hivemind import RecordingMind, Action


class WorldObject(object):

    def __init__(self, 
        x, 
        y, 
        color, 
        facing, 
        health=3, 
        scale=1, 
        damagable=True, 
        moveable=True, 
        spawner=None,
        *args,
        **kwargs):

        self.health = health
        self.x = x
        self.y = y
        self.color = color
        self.scale = scale
        self.damagable = damagable
        self.moveable = moveable
        self.facing = facing
        self.mind = RecordingMind()
        self.spawned_by = spawner

        self._square_cache = {}
        self._section_cache = {}
        #TODO
        self._last_hit_by = None

        self._regsiter_actions()
        

    def _regsiter_actions(self):
        """ Very very very very hacky. Turn your eyes away here """
        from types import MethodType as instancemethod
        for func_name in dir(self):
            try:
                func = self.__getattribute__(func_name)
            except:
                pass
            if isinstance(func, instancemethod):
                try:
                    if 'action' in func.func_dict:
                        self.mind.register_action(func, func.func_dict['type'])
                except AttributeError:
                    pass

    def tick(self, world):
        pass

    @Action("Death", class_watch=['_last_hit_by'])
    def die(self):
        pass

    def _debug_draw(self):
        if (self.x, self.y, self.facing) not in self._section_cache:
            self._section_cache[(self.x, self.y, self.facing)] = into_sections(self.populated_squares)

        gl.glPushMatrix()

        for square in self.populated_squares:
            x, y, color = square
            r, g, b =color

            gl.glColor3f(r, g, b)
            draw_square(x, y)

        gl.glPopMatrix() 


    def draw(self):
        """ draw method used to draw all the populated squares 
            by this object - uses clever caching and sections to improve 
            draw speed """

        if (self.x, self.y, self.facing, self.scale) not in self._section_cache:
            self._section_cache[(self.x, self.y, self.facing, self.scale)] = into_sections(self.populated_squares)

        gl.glPushMatrix()

        for section in self._section_cache[(self.x, self.y, self.facing, self.scale)]:
            (x, y, width, height, color) = section
            r, g, b = color
            gl.glColor3f(r, g, b)
            draw_square(x, y, width, height)

        gl.glPopMatrix() 

    @Action("taking damage", class_watch=['_last_hit_by'])
    def take_damage(self, damage, other):
        self.health -= damage
        self._last_hit_by = other

    def deal_damage(self, other):
        pass

    @Action("Moving", watch={1 : 'facing', 2 : 'distance'})
    def move(self, world, facing, distance=1):
        if facing == DIRECTIONS['still']:
            return
        world.move_in_direction(self, facing, distance)

    def populated_at(self, x, y):
        """ returns a list of tuples containing the coordinates of populated 
            squares, should the square be at this point
        """
        return [(x, y, self.color)]

    @property
    def populated_squares(self):
        """ returns the populated squares for the current object 
            clever caching method """
        if (self.x, self.y, self.facing, self.scale) not in self._square_cache:
            self._square_cache[(self.x, self.y, self.facing, self.scale)] = self.populated_at(self.x, self.y)
        return self._square_cache[(self.x, self.y, self.facing, self.scale)]

    def closest_point(self, x, y):
        """ returns the coordinates which are part of this object and
            closest to x, y """
        x2nd = x ** 2
        y2nd = y ** 2
        euclid = lambda i, j: (x2nd - (i ** 2)) + (y2nd - (j ** 2))

        small_score = 9000001
        smallest = None

        for (x, y) in self.populated_squares:
            score = euclid(x, y)
            if score < small_score:
                smallest = (x, y)
                small_score = score
        return smallest


