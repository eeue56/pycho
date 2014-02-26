from pycho.world_objects import known_objects

def register_object(object_name, object_class):
    known_objects[object_name] = object_class

def box_around(x, y, width, height):

    populated = []
    populate = lambda i, j : populated.append((i, j, None))

    for i in range(x - width, x + width):
        for j in range(y - height, y + height):
            populate(i, j)
    return populated