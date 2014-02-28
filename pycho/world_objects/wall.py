from __future__ import division

from pycho.world_objects import WorldObject
from pycho.world.navigation import DIRECTIONS

from pycho.gl.color import COLORS

from pycho.gl.drawing import generate_rectangle_vbo, draw_vbo

import OpenGL.GL as gl


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

        self.vbo = generate_rectangle_vbo(*self.vbo_points())

    def vbo_points(self):
        populated = self.populated_at()

        min_x = self.x
        min_y = self.y

        max_x = 0
        max_y = 0

        for (x, y, _) in populated:
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y

        if max_x < min_x:
            max_x, min_x = min_x, max_x

        if max_y < min_y:
            max_y, min_y = min_y, max_y

        print('Facing: ', self.facing)
        print('Min x:', min_x)
        print('Min y:', min_y)
        print('Max x:', max_x)
        print('Max y:', max_y)

        return (min_x, min_y, max_x - min_x, max_y - min_y)


    def tick(self, world):
        pass

    def take_damage(self, damage, world):
        pass

    def draw(self):

        gl.glPushMatrix()


        r, g, b = self.color
        gl.glColor3f(r, g, b)
        draw_vbo(self.vbo)

        gl.glPopMatrix() 

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