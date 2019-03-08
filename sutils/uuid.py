import string
import random


SUFFIX_CHARS = string.ascii_lowercase + string.digits


def simple_uuid(length=8):
    return "".join(random.choices(SUFFIX_CHARS, k=length))
