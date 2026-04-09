#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Global imports
import re
import requests

# Local imports
import utils


# TODO: optimise auth
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


def blob_exists(url):
    try:
        blob_get(url)
        return True
    except:
        return False


def blob_get(url):
    s = authenticate("https://management.core.windows.net/")
    r = s.get(url, headers=blob_headers())
    r.raise_for_status()
    return r.text


def blob_list(url, prefix, metadata=True):
    s = authenticate("https://management.core.windows.net/")
    p = {
        'restype': 'container',
        'comp':    'list',
        'prefix':  prefix,
    }
    if metadata:
        p['include'] = 'metadata'

    try:
        r = s.get(url, headers=blob_headers(), params=p)
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

    blobs = utils.str_between(xml, '<Blobs>', '</Blobs>')
    if blobs is None:
        return r

    for blob in blobs.split('<Blob>'):
        blob_name = utils.str_between(blob, '<Name>', '</Name>')
        if blob_name is None:
            continue
        r[blob_name] = {}

        metadatas = utils.str_between(blob, '<Metadata>', '</Metadata>')
        if metadatas:
            pairs = re.findall(r"<(\w+)>(.*?)</\1>", metadatas)
            if len(pairs) > 0:
                r[blob_name] = dict(pairs)

    return r


if "__main__" == __name__:
    from pprint import pprint
    xml="""
<?xml version="1.0" encoding="utf-8"?>
<EnumerationResults ServiceEndpoint="http://myaccount.blob.core.windows.net/"  ContainerName="mycontainer">
  <Prefix>string-value</Prefix>
  <Marker>string-value</Marker>
  <MaxResults>int-value</MaxResults>
  <Delimiter>string-value</Delimiter>
  <Blobs>
    <Blob>
      <Name>blob-name</Name>
      <Snapshot>date-time-value</Snapshot>
      <VersionId>date-time-vlue</VersionId>
      <IsCurrentVersion>true</IsCurrentVersion>
      <Deleted>true</Deleted>
      <Properties>
        <Creation-Time>date-time-value</Creation-Time>
        <Last-Modified>date-time-value</Last-Modified>
        <Etag>etag</Etag>
        <Owner>owner user id</Owner>
      </Properties>
      <Metadata>
        <Name>value</Name>
        <User>toto@toto</User>
      </Metadata>
      <Tags>
          <TagSet>
              <Tag>
                  <Key>TagName</Key>
                  <Value>TagValue</Value>
              </Tag>
          </TagSet>
      </Tags>
      <OrMetadata />
    </Blob>
    <BlobPrefix>
      <Name>blob-prefix</Name>
    </BlobPrefix>
  </Blobs>
  <NextMarker />
</EnumerationResults>  """
    r = blob_list_parse(xml)
    assert(r == {'blob-name': {'Name': 'value', 'User': 'toto@toto'}})
    pprint(r)
