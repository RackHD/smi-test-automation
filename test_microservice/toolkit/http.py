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

LOG = logging.getLogger(__name__)

JSON_HEADER = {'Content-Type': 'application/json'}

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

def missing_parameter_combos(payload):
    """Generate all combinations of missing paramters"""
    for count, _ in enumerate(payload):
        for key_combo in itertools.combinations(payload, count):
            bad_dict = {key: payload[key] for key in key_combo}
            yield bad_dict

def empty_parameter_combos(payload):
    """Generate all combinations of empty paramters"""
    for count, _ in enumerate(payload):
        for key_combo in itertools.combinations(payload, count):
            result = payload.copy()
            for key in result:
                if key not in key_combo:
                    result[key] = ''
            yield result

def rest_get_url(url):
    """Make a GET rest call to the specified URL"""
    LOG.debug("Calling GET: %s", url)
    response = requests.get(url, headers=JSON_HEADER)
    LOG.debug("Results from GET: %s\n", response)
    return response

def rest_get(url, payload):
    """Make a GET rest call to the specified URL with parameters"""
    LOG.debug("Calling GET: %s Parameters : %s", url, payload)
    response = requests.get(url, headers=JSON_HEADER, params=payload)
    LOG.debug("Results from GET: %s", response)
    return response

def rest_post(url, payload):
    """Make a POST rest call to the specified URL and payload"""
    LOG.debug("Calling POST: %s", url)
    response = requests.post(url, headers=JSON_HEADER, json=payload)
    LOG.debug("Results from POST: %s", response)
    return response
