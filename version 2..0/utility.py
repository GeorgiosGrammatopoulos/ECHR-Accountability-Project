import random
import string

def random_name(length=6):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))
