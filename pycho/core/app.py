from pycho.gui.application import Application as App

from pycho.world import World
from pycho.core.game import Game
from pycho.gui.windows import DefaultWindow

from pycho.world_objects import Player
from pycho.levels import LevelController, generate_objects

from pycho.gl.color import COLORS
from pycho.world.navigation import DIRECTIONS

import logging
import sys



def application(level_file, 
    player_x, 
    player_y, 
    player_color=None, 
    player_direction=None, 
    player_options=None):

    logging.getLogger().setLevel(logging.ERROR)



    with open(level_file) as f:
        levels, player = generate_objects(f.read())


    if player is None:
        if player_options is None:
            player_options = {}

        if player_color is None:
            player_color = COLORS['white']

        if player_direction is None:
            player_direction = DIRECTIONS['up']
        player = Player(player_x, player_y, 
            player_color, player_direction, **player_options)


    level_controller = LevelController(levels)
    world = World(player, level_controller)
    game = Game(player, world)

    app = App(sys.argv)
    window = DefaultWindow(game)
    window.show()

    return (game, app, window)