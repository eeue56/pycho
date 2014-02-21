from collections import OrderedDict

def into_ordered_dict(blocklist):
    """ Puts the blocklist into an ordered dict """
    into_dict = OrderedDict()

    for block in blocklist:
        x, y, color = block
        if y not in into_dict:
            into_dict[y] = OrderedDict()
        into_dict[y][x] = color

    out = OrderedDict()

    for y in sorted(into_dict):
        out[y] = OrderedDict()
        for x in sorted(into_dict[y]):
            out[y][x] = into_dict[y][x]
    return out

def into_sections(blocklist):
    """ Breaks the blocklist down into sections to 
        increase performance of the game, by drawing things
        as large sections rather than singular blocks
    """
    # TODO:
    # goes wrong when
    # x = 0 
    # y > 0, y < max_y
    # TODO: refactor
    into_dict = into_ordered_dict(blocklist)

    sections = []

    for y in into_dict:
        last_x = -1
        last_color = None
        width = 1
        start_x = None

        for x, color in into_dict[y].items():
            if last_color is None:
                last_color = color

            if x == last_x + 1 and color == last_color:
                if start_x is None:
                    last_color = color
                    start_x = x
                else:
                    width += 1
            else:
                if start_x is None:
                    start_x = x

                sections.append((start_x, y, width, 1, last_color))
                
                start_x = None
                last_color = None
                width = 1
                
            last_x = x

        if start_x is None:
            start_x = x

        if last_color is None:
            last_color = color

        sections.append((start_x, y, width, 1, last_color))

    return sections