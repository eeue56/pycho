def color_tuple_to_dict(color):
    return { k : color[i] for i, k in enumerate('rgb') }

def color_dict_to_tuple(color):
    return tuple([color[k] for k in 'rgb'])