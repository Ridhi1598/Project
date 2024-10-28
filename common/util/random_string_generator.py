import random, string
from random import randint


def random_node():
    x = ''.join(random.choice(string.digits) for _ in range(2))
    y = ''.join(random.choice(string.digits) for _ in range(2))
    return 'SRRYBC' + x + 'OT' + y
    # SRRYBC01OT00


def random_lag():
    x = ''.join(random.choice(string.digits) for _ in range(3))
    return 'lag-' + x


class RandomStringGenerator(object):
    '''
    Generates random string and numbers
    '''

    @staticmethod
    def generate_random_pet_name(length):
        return "pet_" + ''.join(random.choice(string.ascii_lowercase) for i in range(length))

    @staticmethod
    def generate_random_numbers(start_index, stop_index):
        return ''.join(str(random.randint(0, 9)) for i in range(start_index, stop_index))

    @staticmethod
    def generate_random_number_with_n_digits(lenght):
        range_start = 10 ** (lenght - 1)
        range_end = (10 ** lenght) - 1
        return randint(range_start, range_end)

    def __init__(self):
        '''
        Constructor
        '''
