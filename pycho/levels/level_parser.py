from json import dumps, loads

from random import choice, randint

from pycho.levels import Level

from pycho.world.navigation import DIRECTIONS
from pycho.world_objects import Wall, known_objects

import logging

try:
    xrange(1)
except NameError:
    xrange = range

def _color_dict_to_tuple(color):
    return color.values()

def _has_trousers(object_data):
    if 'render_trousers' in object_data:
        return object_data['render_trousers']
    return True

def _generate_fixed(level, fixed_records):
    for object_class, object_data in fixed_records.items():

        if object_class not in known_objects:
            logging.warning('no such class as {c}'.format(c=object_class))
            continue

        if not _has_trousers(object_data):
            continue

        if 'color' in object_data:
            object_data['color'] = _color_dict_to_tuple(object_data['color'])
        level.add_object(known_objects[object_class](**object_data))


def _generate_random(level, random_records):
    for object_class, object_data in random_records.items():
        if object_class not in known_objects:
            logging.warning('no such class as {c}'.format(c=object_class))
            continue

        if not _has_trousers(object_data):
            continue

        position_information = object_data['between']

        x = position_information['x']
        y = position_information['y']
        high_x = x + position_information['width']
        high_y = y + position_information['height']
        colors = [color.values() for color in object_data['colors']]

        for _ in xrange(object_data['amount']):
            my_x = randint(x, high_x)
            my_y = randint(y, high_y)
            my_color = choice(colors)

            level.add_object(known_objects[object_class](my_x, my_y, my_color, 0))

def _generate_walls(world_width, world_height, wall_records):

    wall_dict = {}
    walls = []

    Waller = lambda *a, **kw: Wall(world_width, world_height, *a, **kw)

    for wall, wall_data in wall_records.items():

        direction = DIRECTIONS[wall]

        if 'gaps' in wall_data:
            gaps = range(wall_data['gaps']['start'], wall_data['gaps']['end'])
        else:
            gaps = []

        width = wall_data['width']
        wall_dict[direction] = wall_data['leads_to']

        walls.append(Waller(width=width, facing=direction, gaps=gaps))

    return wall_dict, walls


def generate_objects(file_data):
    data = loads(file_data)

    level_dict = {}

    logging.debug("Loading {x} levels from level_data.json!".format(x=len(data)))

    for level_id, level_data in data.items():
        world_width = level_data['width']
        world_height = level_data['height']
        color = _color_dict_to_tuple(level_data['color'])

        wall_dict, walls = _generate_walls(world_width, world_height, level_data['walls'])

        level = Level(color, wall_dict, world_width, world_height)
        level.add_objects(walls)

        if 'fixed' in level_data:
            _generate_fixed(level, level_data['fixed'])

        if 'random' in level_data:
            _generate_random(level, level_data['random'])

        level_dict[int(level_id)] = level

    if len(data) == len(level_dict):
        logging.debug("All levels loaded correctly.")
    else:
        logging.debug("Not all levels loaded properly! {x} out of {y} were loaded!",
            x=len(level_dict),
            y=len(data))


    return level_dict





