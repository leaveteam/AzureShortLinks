#! /usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
## Imports
###############################################################################
# Global
import azure.functions as func

# Local
import config
import filter
import azutils


###############################################################################
## Routes
###############################################################################
app = func.FunctionApp()
@app.route(route="ping", auth_level=func.AuthLevel.ANONYMOUS, methods=[func.HttpMethod.GET])
def test(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("pong", mimetype="text/plain")


@app.route(route="version", auth_level=func.AuthLevel.ANONYMOUS, methods=[func.HttpMethod.GET])
def test(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(config.VERSION, mimetype="text/plain")


@app.route(route="whoami", auth_level=func.AuthLevel.ANONYMOUS, methods=[func.HttpMethod.GET])
def test(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("Hello\ntoto\n", mimetype="text/plain")


@app.route(route="new", auth_level=func.AuthLevel.ANONYMOUS, methods=[func.HttpMethod.GET])
def test(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("Hello\ntoto\n", mimetype="text/plain")


@app.route(route="list", auth_level=func.AuthLevel.ANONYMOUS, methods=[func.HttpMethod.GET])
def test(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("Hello\ntoto\n", mimetype="text/plain")

