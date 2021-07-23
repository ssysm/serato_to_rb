import random


def generate_random_number(length):
    return int(''.join([str(random.randint(0,10)) for _ in range(length)]))
