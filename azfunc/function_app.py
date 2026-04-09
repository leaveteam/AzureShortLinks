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
import httputils
import utils


###############################################################################
## Functions
###############################################################################


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
    return func.HttpResponse(httputils.user_from_req(req), mimetype="text/plain")


@app.route(route="new", auth_level=func.AuthLevel.ANONYMOUS, methods=[func.HttpMethod.GET])
def route_new(req: func.HttpRequest) -> func.HttpResponse:
    # Get params
    user = httputils.user_from_req(req)
    lnk  = httputils.param(req, 'lnk', is_link_id)
    dst  = httputils.param(req, 'dst', is_url)

    # Calculate blob url
    lnkurl = "%s/links/%s" % (config.BLOB_URL, lnk)

    # Check if the redirect blob exists
    if azutils.blob_exists(url):
        return httputils.response(400, {'msg': 'Link already exists'})

    # Get the list of references in the user profile
    usrb64 = utils.b64e(user)
    l = blob_list(config.BLOB_URL, "users/%s/" % usrb64, False)

    # Check is the user as maxed his credit
    if len(l) >= config.MAX_LINKS:
        return httputils.response(400, {'msg': 'Link quota exhaustion'})

    # Create user blob
    azutils.blob_create("%s/users/%s/%s" % (config.BLOB_URL, usrb64, lnk), '')

    # Create redirect blob
    azutils.blob_create(lnkurl, dst)

    # TODO: Log creation

    return func.HttpResponse("done", mimetype="text/plain")


@app.route(route="delete", auth_level=func.AuthLevel.ANONYMOUS, methods=[func.HttpMethod.GET])
def route_delete(req: func.HttpRequest) -> func.HttpResponse:
    # Get params
    user = httputils.user_from_req(req)
    lnk  = httputils.param(req, 'lnk', is_link_id)

    # Compute urls
    permurl = "%s/users/%s/%s" % (config.BLOB_URL, usrb64, lnk)
    lnkurl  = "%s/links/%s"    % (config.BLOB_URL, lnk)

    # Check it the link belongs to the user
    if not azutils.blob_exists(permurl):
        return httputils.response(403, {'msg': 'This link does not belong to you'})

    # Delete the redirect blob
    azutils.blob_delete(lnkurl)

    # Delete the perm blob
    azutils.blob_delete(permurl)

    # TODO: Log creation

    return func.HttpResponse("done", mimetype="text/plain")


@app.route(route="list", auth_level=func.AuthLevel.ANONYMOUS, methods=[func.HttpMethod.GET])
def route_list(req: func.HttpRequest) -> func.HttpResponse:
    user = user_from_req(req)

    lnks = azutils.blob_list(url, b64e(user))
    return func.HttpResponse(lnks.keys(), mimetype="application/json")
