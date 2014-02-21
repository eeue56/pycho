def test_color_converting():
    from pycho.levels.helpers import color_tuple_to_dict, color_dict_to_tuple

    red = (1, 0, 0)

    dict_red = color_tuple_to_dict(red)

    assert dict_red['r'] == red[0]
    assert dict_red['g'] == red[1]
    assert dict_red['b'] == red[2]

    tupled_red = color_dict_to_tuple(dict_red)

    assert tupled_red == red

def main():
    test_color_converting()

if __name__ == '__main__':
    main()