"""Django Model related helpers
"""
from os import urandom
from django.core.signing import b62_encode

def uniqueness(value, separator='-'):
    """Generate unique string prefix
    """
    rando = b62_encode(int.from_bytes(urandom(8)))
    return f'{value}{separator}{rando}'
