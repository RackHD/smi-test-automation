# -*- coding: utf-8 -*-

#   __      ___  ___ _  __ ___          ___ _           ___ ___  _
#  (_  |\/|  | __ | |_ (_   | __ /\  | | | / \ |\/|  /\  |   |  / \ |\ |
#  __) |  | _|_   | |_ __)  |   /--\ |_| | \_/ |  | /--\ |  _|_ \_/ | \|

"""
HTTP Toolkit
~~~~~~~~~~~~
Series of tools designed around HTTP requests

Copyright (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
Created on June 23, 2017
"""
__title__ = 'HTTP Toolkit'
__author__ = 'Akash Kwatra'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2017 DELL Inc.'

import logging
import itertools
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
    base_url += "?"
    for key in parameters:
        value = parameters[key]
        base_url += "{}={}&".format(key, value)
    return base_url[:-1]

def missing_parameter_combinations(parameters):
    """Generate all combinations of missing paramters"""
    for count in len(parameters) - 1:
        for combo in itertools.combinations(parameters, count):
            yield combo

def empty_parameter_combinations(parameters):
    """Generate all combinations of empty paramters"""
    for count in len(parameters) - 1:
        for combo in itertools.combinations(parameters, count):
            result = parameters.copy()
            for key in result:
                if key not in combo:
                    result[key] = ''
            yield result


def rest_get(url):
    """Make a GET rest call to the specified URL"""
    LOG.info("Calling GET: %s", url)
    headers = {'Content-Type': 'application/json'}
    action = 'GET'
    response = _get_response(action, url, None, headers)
    LOG.info("Results from GET: %s\n", response)
    return response

def rest_post(url, payload):
    """Make a POST rest call to the specified URL and payload"""
    LOG.info("Calling POST: %s", url)
    headers = {'Content-Type': 'application/json'}
    action = 'POST'
    response = _get_response(action, url, payload, headers)
    LOG.info("Results from POST: %s\n", response)
    return response

def _get_response(action, url, request_json, headers):
    """Generate an http request and return response"""
    LOG.info("get_response")
    headers = {'Content-Type': 'application/json'}
    if action == "POST":
        LOG.info("POST Request")
        response = requests.post(url, json=request_json, headers=headers)
    elif action == "GET":
        LOG.info("GET Request")
        response = requests.get(url, json=request_json, headers=headers)
    elif action == "PUT":
        LOG.info("PUT Request")
        response = requests.put(url, json=request_json, headers=headers)
    elif action == "DELETE":
        LOG.info("DELETE Request")
        response = requests.delete(url, json=request_json, headers=headers)
    else:
        raise Exception("Invalid Action : " + action)
    LOG.debug("Generated response :: %s", response.text)
    return response


