from pycho.world_objects import known_objects

def register_object(object_name, object_class):
    known_objects[object_name] = object_class