#! /usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
## Imports
###############################################################################
# Global
import azure.functions as func
import base64

# Local
import config
import filter
import azutils



###############################################################################
## Routes
###############################################################################
def user_from_req(req):
    # TODO: get user from token
    return "toto@toto.com"

def b64e(text):
    return base64.urlsafe_b64encode(text.encode("utf-8")).decode("utf-8").rstrip("=")


###############################################################################
## Routes
###############################################################################
app = func.FunctionApp()
@app.route(route="ping", auth_level=func.AuthLevel.ANONYMOUS, methods=[func.HttpMethod.GET])
def route_ping(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("pong", mimetype="text/plain")


@app.route(route="version", auth_level=func.AuthLevel.ANONYMOUS, methods=[func.HttpMethod.GET])
def route_version(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(config.VERSION, mimetype="text/plain")


@app.route(route="whoami", auth_level=func.AuthLevel.ANONYMOUS, methods=[func.HttpMethod.GET])
def route_whoami(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(user_from_req(req), mimetype="text/plain")


@app.route(route="new", auth_level=func.AuthLevel.ANONYMOUS, methods=[func.HttpMethod.GET])
def route_new(req: func.HttpRequest) -> func.HttpResponse:
    # Check if the redirect blob exists

    # Get the list of references in the user profile

    # Check is the user as maxed his credit

    # Check it it belongs to the user

    # Create redirect blob

    # Log creation

    return func.HttpResponse("done", mimetype="text/plain")


@app.route(route="delete", auth_level=func.AuthLevel.ANONYMOUS, methods=[func.HttpMethod.GET])
def route_delete(req: func.HttpRequest) -> func.HttpResponse:
    # Get the list of references in the user profile

    # Check it the link belongs to the user

    # Delete the redirect blob

    # Log creation

    return func.HttpResponse("done", mimetype="text/plain")


@app.route(route="list", auth_level=func.AuthLevel.ANONYMOUS, methods=[func.HttpMethod.GET])
def route_list(req: func.HttpRequest) -> func.HttpResponse:
    user = user_from_req(req)

    lnks = azutils.blob_list(url, b64e(user))
    return func.HttpResponse(lnks.keys(), mimetype="application/json")
