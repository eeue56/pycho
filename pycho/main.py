from pycho.world import World
from pycho.core.game import Game
from pycho.gui.windows import DefaultWindow
from pycho.gui.application import Application

from pycho.world_objects import Player
from pycho.levels import LevelController, generate_objects

from pycho.gl.color import COLORS
from pycho.world.navigation import DIRECTIONS
 

if __name__ == '__main__':
    import sys
    import logging

    logging.getLogger().setLevel(logging.ERROR)

    player = Player(50, 50, COLORS['white'], DIRECTIONS['up'], speed=2)

    with open('level_data.json') as f:
        levels = generate_objects(f.read())

    level_controller = LevelController(levels[0], levels)
    world = World(player, level_controller)
    game = Game(player, world)

    app = Application(sys.argv)
    window = DefaultWindow(game)
    window.show()
    app.exec_()