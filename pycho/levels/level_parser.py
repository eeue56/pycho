from json import dumps, loads
from copy import deepcopy

from random import choice, randint

from functools import partial

from pycho.levels import Level
from pycho.levels.helpers import *

from pycho.world.navigation import DIRECTIONS
from pycho.world_objects import Wall, known_objects

import logging

try:
    xrange(1)
except NameError:
    xrange = range

# level defaults
DEFAULT_LEVEL_VALUES = {
    'width' : 100,
    'height' : 100,
    'color' : { 'r' : 0,
                'g' : 0,
                'b' : 0
    },
    'is_first' : False,
    'fixed' : {},
    'random' : {},
    'walls' : {}
}

def load_defaults_from_file(filename=None):
    if filename is None:
        filename = 'defaults.json'

    try:
        with open(filename) as f:
            logging.debug('Reading defaults from {}'.format(filename))
            return loads(f.read())
    except IOError:
        logging.debug('Using hardcoded defaults')
        return DEFAULT_LEVEL_VALUES

def _has_trousers(object_data):
    if 'render_trousers' in object_data:
        return object_data['render_trousers']
    return True

def _generate_fixed(level, fixed_records):
    player = None

    for object_class, object_data_list in fixed_records.items():
        if object_class not in known_objects:
            logging.warning('no such class as {c}'.format(c=object_class))
            continue

        for object_data in object_data_list:
            if not _has_trousers(object_data):
                continue

            if 'color' in object_data:
                object_data['color'] = color_dict_to_tuple(object_data['color'])
            obj_ = known_objects[object_class](**object_data)
            level.add_object(obj_)

            if object_class == 'player':
                player = obj_
    return player


def _generate_random(level, random_records):
    for object_class, object_data_list in random_records.items():
        if object_class not in known_objects:
            logging.warning('no such class as {c}'.format(c=object_class))
            continue

        for object_data in object_data_list:
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

    Waller = partial(Wall, world_width, world_height)

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

def _load_defaults(default_dict, level_data):
    defaults = deepcopy(default_dict)
    defaults.update(level_data)
    return defaults


def load_level(level_id, level_data):
    world_width = level_data['width']
    world_height = level_data['height']
    color = color_dict_to_tuple(level_data['color'])

    is_first = level_data['is_first']

    wall_dict, walls = _generate_walls(world_width, 
        world_height, level_data['walls'])

    level = Level(color, wall_dict, world_width, world_height, is_first=is_first, level_id=level_id)
    
    if walls:
        level.add_objects(walls)

    _player = _generate_fixed(level, level_data['fixed'])
    _generate_random(level, level_data['random'])

    return level, _player

def generate_objects(file_data, defaults_filename=None):

    defaults = load_defaults_from_file(defaults_filename)
    default_loader = partial(_load_defaults, defaults)

    data = loads(file_data)

    level_dict = {}

    logging.debug("Loading {x} levels from level_data.json!".format(x=len(data)))

    player = None

    for level_id, level_data in data.items():
        level_data = default_loader(level_data)

        level, _player = load_level(level_id, level_data)
        level_dict[level_id] = level

        if _player is not None:
            player = _player

    if len(data) == len(level_dict):
        logging.debug("All levels loaded correctly.")
    else:
        logging.debug("Not all levels loaded properly! {x} out of {y} were loaded!",
            x=len(level_dict),
            y=len(data))


    return (level_dict, player)