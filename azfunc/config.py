#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os


VERSION="0.0.1"

BLOB_URL  = os.getenv('BLOB_URL')
MAX_LINKS = int(os.getenv('MAX_LINKS', 10))
