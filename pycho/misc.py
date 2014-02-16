from __future__ import division

import OpenGL.GL as gl

from random import randint

from collections import OrderedDict

try:
    xrange(0)
except NameError:
    xrange = range


COLOURS = { 
    'black' : (0, 0, 0),
    'other-grey' : (0.25, 0.25, 0.25),
    'grey' : (0.4, 0.4, 0.4),
    'red' :  (255, 0, 0),
    'white' : (1, 1, 1)
}

DIRECTIONS = {
    'still' : 0,
    'up' : 1,
    'down' : -1,
    'right' : 20,
    'left' : -20,
    'up-left' : -19,
    'up-right' : 21,
    'down-left' : -21,
    'down-right' : 19
}

MOVEMENTS = {
    DIRECTIONS['still'] : (0, 0),
    DIRECTIONS['up'] : (0, 1),
    DIRECTIONS['down'] : (0, -1),
    DIRECTIONS['left'] : (-1, 0),
    DIRECTIONS['right'] : (1, 0),
    DIRECTIONS['up'] + DIRECTIONS['left'] : (-1, 1),
    DIRECTIONS['up'] + DIRECTIONS['right'] : (1, 1),
    DIRECTIONS['down'] + DIRECTIONS['left'] : (-1, -1),
    DIRECTIONS['down'] + DIRECTIONS['right'] : (1, -1)
}

def opposite_direction(direction):
    """ Returns the opposite direction """
    return -direction

def random_color():
    """ Returns a colour tuple """
    return tuple(y / 255 for y in (randint(0, 255), randint(0, 255), randint(0, 255)))

def draw_square(x, y, x_size=1, y_size=1):
    """ Draw a square of given location and size """
    gl.glRectf(x, y, x + x_size, y + y_size)

def into_ordered_dict(blocklist):
    """ Puts the blocklist into an ordered dict """
    into_dict = OrderedDict()

    for block in blocklist:
        x, y, color = block
        if y not in into_dict:
            into_dict[y] = OrderedDict()
        into_dict[y][x] = color

    out = OrderedDict()

    for y in sorted(into_dict):
        out[y] = OrderedDict()
        for x in sorted(into_dict[y]):
            out[y][x] = into_dict[y][x]
    return out

def into_sections(blocklist):
    """ Breaks the blocklist down into sections to 
        increase performance of the game, by drawing things
        as large sections rather than singular blocks
    """
    # TODO:
    # goes wrong when
    # x = 0 
    # y > 0, y < max_y
    # TODO: refactor
    into_dict = into_ordered_dict(blocklist)

    sections = []

    for y in into_dict:
        last_x = -1
        last_color = None
        width = 1
        start_x = None

        for x, color in into_dict[y].items():
            if last_color is None:
                last_color = color

            if x == last_x + 1 and color == last_color:
                if start_x is None:
                    last_color = color
                    start_x = x
                else:
                    width += 1
            else:
                if start_x is None:
                    start_x = x

                sections.append((start_x, y, width, 1, last_color))
                
                start_x = None
                last_color = None
                width = 1
                
            last_x = x

        if start_x is None:
            start_x = x

        if last_color is None:
            last_color = color

        sections.append((start_x, y, width, 1, last_color))

    return sections