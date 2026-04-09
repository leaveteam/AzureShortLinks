#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re


def is_link_id(txt):
    return re.match('^[_-0-9a-fA-F]{5,64}$', txt) is not None

def is_url(txt):
    return re.match('^https:\/\/([a-zA-Z0-9-]{2,99}\.){1,8}[a-zA-Z]{2,}(:\d{0,5})?(\/[^\s]{512})?$', txt) is not None

def is_user(txt):
    return re.match('^[a-zA-Z0-9._%+-]{2,256}@[a-zA-Z0-9.-]{1,256}\.[a-zA-Z]{2,32}$', txt) is not None
