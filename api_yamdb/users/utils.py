from random import randint


def get_confirmation_code():
    return str(randint(10000, 99999))