from PyQt5.QtCore import Qt as Q

QT_KEYS = {k[4:]: Q.__getattribute__(Q, k) for k in dir(Q) if k.startswith('Key_')}

LEFT_KEYS = (QT_KEYS['A'], QT_KEYS['Left'])
RIGHT_KEYS = (QT_KEYS['D'], QT_KEYS['Right'])
UP_KEYS = (QT_KEYS['W'], QT_KEYS['Up'])
DOWN_KEYS = (QT_KEYS['S'], QT_KEYS['Down'])

def is_left(key, left_keys=LEFT_KEYS):
    return key in left_keys
    
def is_right(key, right_keys=RIGHT_KEYS):
    return key in right_keys

def is_up(key, up_keys=UP_KEYS):
    return key in up_keys

def is_down(key, down_keys=DOWN_KEYS):
    return key in down_keys