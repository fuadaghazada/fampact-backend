import random


def boolean(string):
    """
    Boolean function convert the string to Python bool type
    :param string:
    :return:
    """

    response = None
    if string == 0:
        response = False
    if string == 1:
        response = True

    if isinstance(string, str):
        if string.lower() in ["0", "no", "false"]:
            response = False
        if string.lower() in ["1", "yes", "true"]:
            response = True

    return response


def random_code(length=4):
    """Generating a random code with the given length (default: 4)"""

    chars = list('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    code = ""
    for i in range(length):
        code += random.choice(chars)

    return code
