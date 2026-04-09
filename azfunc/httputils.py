#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json


class HttpError(Exception):
    def __init__(self, status_code, message):
        super().__init__(message)
        self.status_code = status_code
        self.message     = message

    def __str__(self):
        return "HttpError(%s): %s" % (self.status_code, self.message)


def user_from_req(req):
    # Get the token from the Authorization header
    bearer = req.headers.get('authorization')
    if not bearer:
        raise HttpError(401, 'Missing authentication')

    # Extract the token
    elts = bearer.split(" ", 1)
    if (len(elts) < 2) or (elts[0] != "Bearer"):
        raise HttpError(401, "Bad authentication format")

    # Parse the token parameters
    jwt  = elts[1]
    elts = jwt.split('.')
    data = json.loads(utils.b64d(elts[1]))

    # Get user from token
    user = data['unique_name']

    # Check id format
    if not is_user(user):
        raise HttpError(401, "Invalid user format")

    return user


def param(req, name, flt, msg="", default=None, optional=False):
    if msg == "":
        msg = "Invalid value for %s" % name

    tmp = req.get(name)
    if tmp is None:
        if optional:
            return default
        else:
            raise HttpError(error_code, msg)

    if not flt(tmp):
        raise HttpError(error_code, msg)

    return tmp


def response(code, data):
    return HttpResponse(json.dumps(data, indent=2),
                        status_code=code,
                        mimetype="application/json")
