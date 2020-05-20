# -*- coding: utf-8 -*-
from hashlib import md5


def get_md5(value):
    if value:
        return md5(value.encode()).hexdigest()
    return ''