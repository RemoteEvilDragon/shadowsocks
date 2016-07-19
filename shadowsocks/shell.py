#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2015 clowwindy
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import, division, print_function, \
    with_statement

import os
import json
import sys
import getopt
import logging
from shadowsocks.common import to_bytes, to_str, IPNetwork
from shadowsocks import encrypt

VERBOSE_LEVEL = 5

verbose = 0

# "server":"27.126.181.90",
# "server_port":61234,
# "server_pwd":"my_name_athen",
# "server_method":"aes-256-cfb"
# "local":"0.0.0.0",
# "local_port":1080,
# "local_pwd":"my_name_athen",
# "local_method":"aes-256-cfb"
# "timeout":300,

def print_exception(e):
    global verbose
    logging.error(e)
    if verbose > 0:
        import traceback
        traceback.print_exc()

def check_config(config):
    encrypt.try_cipher(config['password'], config['method'])

def get_config():
    global verbose
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-s: %(message)s')
   
    config_path = sys.argv[1]

    logging.info('loading config from %s' % config_path)
    with open(config_path, 'rb') as f:
        try:
            config = parse_json_in_str(f.read().decode('utf8'))
        except ValueError as e:
            logging.error('found an error in config.json: %s',e.message)
            sys.exit(1)

    check_config(config)
    return config

def _decode_list(data):
    rv = []
    for item in data:
        if hasattr(item, 'encode'):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.items():
        if hasattr(value, 'encode'):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv

def parse_json_in_str(data):
    # parse json and convert everything from unicode to str
    return json.loads(data, object_hook=_decode_dict)
