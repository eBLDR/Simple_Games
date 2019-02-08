def _display(title: str, dict_: dict, left_width: int = 20, right_width: int = 10):
    dot = '.'
    print(' {} '.format(title.upper()).center(left_width + right_width, '='))
    for key, value in dict_.items():
        if key in ['max_health', 'max_energy']:
            continue
        elif key in ['health', 'energy']:
            print((key.replace('_', ' ').title() + ' ').ljust(left_width, dot) + ' {}/{}'.format(dict_[key], dict_['max_{}'.format(key)]).rjust(right_width, dot))
        else:
            print((key.replace('_', ' ').title() + ' ').ljust(left_width, dot) + ' {}'.format(value).rjust(right_width, dot))

        if key == 'level':
            print('-' * (left_width + right_width))
    print()


def display_stats(stats: dict):
    _display('stats', stats)


def display_equipment(equipment: dict):
    _display('equipment', equipment)
