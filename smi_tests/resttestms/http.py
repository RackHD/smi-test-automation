# -*- coding: utf-8 -*-
"""
HTTP Toolkit
~~~~~~~~~~~~
Series of tools designed around HTTP requests

:Copyright: (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
:License: Apache 2.0, see LICENSE for more details.
:Author: Akash Kwatra

Created on June 23, 2017
"""

import logging
import itertools
import requests
from . import json

LOG = logging.getLogger(__name__)

JSON_HEADER = {'Content-Type': 'application/json'}

###################################################################################################
# Initialize Class Data
###################################################################################################

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

###################################################################################################
# Generate Request Data
###################################################################################################

def missing_data_combos(payload):
    """Generate all combinations of missing data"""
    for count, _ in enumerate(payload):
        for key_combo in itertools.combinations(payload, count):
            bad_dict = {key: payload[key] for key in key_combo}
            yield bad_dict

def empty_data_combos(payload):
    """Generate all combinations of empty data"""
    for count, _ in enumerate(payload):
        for key_combo in itertools.combinations(payload, count):
            result = payload.copy()
            for key in result:
                if key not in key_combo:
                    result[key] = ''
            yield result

###################################################################################################
# Make Requests
###################################################################################################

def rest_get(url, parameters):
    """Make a GET rest call to the specified URL with parameters"""
    LOG.info("==== GET ==== :: URL : %s :: PARAMETERS : %s", url, parameters)
    response = requests.get(url, headers=JSON_HEADER, params=parameters)
    LOG.info("RESPONSE :: %s", json.load_response_data(response))
    return response

def rest_post(url, payload):
    """Make a POST rest call to the specified URL and payload"""
    LOG.info("==== POST ==== :: URL : %s :: PAYLOAD : %s", url, payload)
    response = requests.post(url, headers=JSON_HEADER, json=payload)
    LOG.info("RESPONSE :: %s", json.load_response_data(response))
    return response

def rest_put(url, payload):
    """Make a PUT rest call to the specified URL and payload"""
    LOG.info("==== PUT ==== :: URL : %s :: PAYLOAD : %s", url, payload)
    response = requests.put(url, headers=JSON_HEADER, json=payload)
    LOG.info("RESPONSE :: %s", json.load_response_data(response))
    return response

def rest_patch(url, payload):
    """Make a PATCH rest call to the specified URL and payload"""
    LOG.info("==== PATCH ==== :: URL : %s :: PAYLOAD : %s", url, payload)
    response = requests.patch(url, headers=JSON_HEADER, json=payload)
    LOG.info("RESPONSE :: %s", json.load_response_data(response))
    return response

def rest_delete(url, payload):
    """Make a DELETE rest call to the specified URL and payload"""
    LOG.info("==== DELETE ==== :: URL : %s :: PAYLOAD : %s", url, payload)
    response = requests.delete(url, headers=JSON_HEADER, json=payload)
    LOG.info("RESPONSE :: %s", json.load_response_data(response))
    return response

def rest_call(action, url, payload):
    """Make the appropriate rest call base on the provided action"""
    action = str(action).upper()
    if action == 'GET':
        return rest_get(url, payload)
    elif action == 'POST':
        return rest_post(url, payload)
    elif action == 'PUT':
        return rest_put(url, payload)
    elif action == 'PATCH':
        return rest_patch(url, payload)
    elif action == 'DELETE':
        return rest_delete(url, payload)
    else:
        LOG.error("Invalid Rest Call : %s", action)
        return rest_get(url, payload)
    