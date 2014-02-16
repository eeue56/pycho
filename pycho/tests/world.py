from pycho.world import register_object

def test_known_objects():
    register_object('fish', object)

    from pycho.world_objects import known_objects

    assert 'fish' in known_objects

def main():
    test_known_objects()