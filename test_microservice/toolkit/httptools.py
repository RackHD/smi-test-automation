# -*- coding: utf-8 -*-

#   __      ___  ___ _  __ ___          ___ _           ___ ___  _
#  (_  |\/|  | __ | |_ (_   | __ /\  | | | / \ |\/|  /\  |   |  / \ |\ |
#  __) |  | _|_   | |_ __)  |   /--\ |_| | \_/ |  | /--\ |  _|_ \_/ | \|

"""
HTTP Toolkit
~~~~~~~~~~~~
Series of tools designed aroudn HTTP

Copyright (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 23, 2017
"""
__title__ = 'httptools'
__author__ = 'Akash Kwatra'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2017 DELL Inc.'

import logging
import requests

LOG = logging.getLogger(__name__)

def select_host(default_host, override):
    """Compare default host and override to determine host"""
    LOG.debug("Default Host :: %s Override :: %s", default_host, override)
    host = override if override else default_host
    LOG.info("Selected host was %s", host)
    return host

def create_base_url(host, port):
    """Use the host and port, generate a url"""
    LOG.debug("Provided Host: %s Port: %s", host, port)
    formatted_host = "http://{}:{}".format(host, port)
    LOG.debug("Generated URL :: %s", formatted_host)
    return formatted_host

def add_query_parameters(base_url, parameters):
    """Add query parameters to http get request"""
    url += "?"
    for key in parameters:
        value = parameters[key]
        url += "{}={}".format(key, value)
        url += '&'
    url -= '&'
    return url

def get_response(action, url, request_json, headers):
    """Generate an http request and return response"""
    LOG.info("get_response")
    headers = {'Content-Type': 'application/json'}
    if action == "POST":
        LOG.info("POST")
        response = requests.post(url, json=request_json, headers=headers)
    elif action == "GET":
        LOG.info("GET")
        response = requests.get(url, json=request_json, headers=headers)
    elif action == "PUT":
        LOG.info("PUT")
        response = requests.put(url, json=request_json, headers=headers)
    elif action == "DELETE":
        LOG.info("DELETE")
        response = requests.delete(url, json=request_json, headers=headers)
    else:
        raise Exception("Invalid Action : " + action)
    LOG.debug("Generated response :: %s", response.txt)
    return response

