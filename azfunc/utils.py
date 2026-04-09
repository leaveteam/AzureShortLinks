#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Global imports
import base64


def str_between(text, start, end):
    if (text is None) or len(text) == 0:
        return None

    s = text.find(start)
    if s < 0:
        return None

    s += len(start)
    if s >= len(text):
        return None

    if (end is None) or (len(end) == 0):
        return text[s:]

    e = text.find(end, s)
    if e < 0:
        return text[s:]

    return text[s:e]


def b64e(text):
    return base64.urlsafe_b64encode(text.encode("utf-8")).decode("ascii").rstrip("=")

def b64d(text):
    text += "="*(len(text) % 4)
    return base64.urlsafe_b64decode(text.encode("ascii")).decode("utf-8")


if '__main__' == __name__:
    assert('a'    == b64d(b64e('a')))
    assert('ab'   == b64d(b64e('ab')))
    assert('abc'  == b64d(b64e('abc')))
    assert('abcd' == b64d(b64e('abcd')))

    assert(str_between('', '', '') is None)
    assert(str_between('abcd',     'a', 'd') == "bc")
    assert(str_between('zzabcdef', 'a', 'd') == "bc")
    assert(str_between('zzabcdef', 'a', 'g') == "bcdef")
    assert(str_between('zzabcdef', 'a', '')  == "bcdef")
    assert(str_between('zzabcdef', '', 'b')  == "zza")
