# Set of utils, functions


def input_boolean(prompt):
    """
    Returns a boolean based on user's input.
    :param prompt: <str> input's prompt
    :return: <bool> based on input
    """
    while True:
        value = input('(y/n) ' + prompt).lower()
        if value in ['y']:
            return True
        elif value in ['n']:
            return False


def input_number(prompt, float_=False):
    """
    Returns a valid integer input.
    :param prompt: <str> input's prompt
    :param float_: <bool> returns a float instead
    :return: <int>/<float> value
    """
    while True:
        number = input(prompt)
        if float_:
            if number.replace('.', '', 1).isdigit():
                return float(number)
        elif number.isdigit():
            return int(number)


def input_action(actions, name=''):
    """
    Returns the value of a valid key input.
    :param actions: <dict> valid set of options
    :param name: <str> player's name
    :return: <str> key's corresponding value
    """
    while True:
        prompt = '\t{}\'s action: '.format(name) if name else '\tAction: '
        action = input(prompt).upper()
        if action in actions.keys():
            return actions[action]
