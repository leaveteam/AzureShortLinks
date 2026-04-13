#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import re


def is_link_id(s):
    return re.match(r'^[_-0-9a-fA-F]{5,64}$', s) is not None

def is_url(s):
    return re.match(r'^https:\/\/([a-zA-Z0-9-]{2,99}\.){1,8}[a-zA-Z]{2,}(:\d{0,5})?(\/[^\s]{512})?$', s) is not None

def is_user_upn(s):
    return re.match(r'^[a-zA-Z0-9._%+-]{2,256}@[a-zA-Z0-9.-]{1,256}\.[a-zA-Z]{2,32}$', s) is not None

def is_user_oid(s):
    return re.match(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$', s) is not None
