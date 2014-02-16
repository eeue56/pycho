__all__ = ['player', 'world_object', 'wall', 'bomb', 'old_grumper', 'word']

from pycho.world_objects.world_object import *

from pycho.world_objects.bomb import *
from pycho.world_objects.wall import *

from pycho.world_objects.word import *

from pycho.world_objects.old_grumper import *
from pycho.world_objects.player import *

known_objects = {
    'bomb' : Bomb,
    'wall' : Wall,
    'old_grumper' : OldGrumper,
    'word' : Word
}