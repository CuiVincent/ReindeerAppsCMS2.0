__author__ = 'cui'

import hashlib

def to_md5(key):
    hash = hashlib.md5(key.encode(encoding='utf-8'))
    return hash.hexdigest()