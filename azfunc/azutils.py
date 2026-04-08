#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import requests



def authenticate(scope):
    url  = 'http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=%s' % scope
    resp = requests.get(url, headers={'Metadata': 'true'})
    resp.raise_for_status()

    token   = resp.json()['access_token']
    session = requests.session()
    session.headers.update({'Authorization': 'Bearer %s' % token})
    session.headers.update({'Content-type': 'application/json'})
    return session


def blob_headers():
    return {
        'x-ms-date':      datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
        'x-ms-version':   '2026-02-06',
        'x-ms-blob-type': 'BlockBlob',
    }

def blob_create(url, content, meta=None):
    s = authenticate("https://management.core.windows.net/")
    h = blob_headers()

    if meta:
        for k, v in meta.items():
            h["x-ms-meta-%s" % k] = v

    r = s.put(url, headers=h, data=content)
    r.raise_for_status()


def blob_delete(url):
    s = authenticate("https://management.core.windows.net/")
    r = s.delete(url, headers=blob_headers())
    r.raise_for_status()


def blob_list(url, prefix):
    s = authenticate("https://management.core.windows.net/")
    u = '%s?restype=container&comp=list&prefix=%s&include=metadata' % (url, prefix)
    try:
        r = s.get(u, headers=blob_headers())
        r.raise_for_status()
        #TODO: Follow tokens
        return blob_list_parse(r.text)
    except:
        print('Unable to access %s' % url)
    return {}


def blob_list_parse(xml):
    r = {}

    if len(xml) < 1:
        return r

    blobs = str_between(xml, '<Blobs>', '</Blobs>')
    if blobs is None:
        return r

    for blob in blobs.split('<Blob>'):
        blob_name = str_between(blob, '<Name>', '</Name>')
        if blob_name is None:
            continue
        r[blob_name] = {}

        metadatas = str_between(blob, '<Metadata>', '</Metadata>')
        pairs     = re.findall(r"<(\w+)>(.*?)</\1>", metadatas)
        if len(pairs) > 0:
            r[blob_name] = dict(pairs)

    return r


def str_between(text, start, end):
    if text is None:
        return None

    s = text.find(start)
    if s < 0:
        return None

    s += len(start)
    if s >= len(text):
        return None

    if end is None:
        return text[s:]

    e = text.find(end, s)
    if e < 0:
        return text[s:]

    return text[s:e]
