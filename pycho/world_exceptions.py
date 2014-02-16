class CollisionException(Exception):
    def __init__(self, other, *args):
        Exception.__init__(self, *args)
        self.other = other

class OutOfWorldException(Exception):
    pass