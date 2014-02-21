from random import randint

COLORS = { 
    'black' : (0, 0, 0),
    'other-grey' : (0.25, 0.25, 0.25),
    'grey' : (0.4, 0.4, 0.4),
    'red' :  (255, 0, 0),
    'white' : (1, 1, 1)
}

def random_color():
    """ Returns a colour tuple """
    return tuple(y / 255 for y in (randint(0, 255), randint(0, 255), randint(0, 255)))