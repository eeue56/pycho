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