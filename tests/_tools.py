import random
import string

def random_word(n, chars = None):
    if chars is None:
        chars = string.ascii_lowercase + string.ascii_uppercase + " "
    word = ""
    for i in range(n):
        word += random.choice(chars)
    return word