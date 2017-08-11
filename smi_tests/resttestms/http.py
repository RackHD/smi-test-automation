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
# Generate Request Data
###################################################################################################

def empty_data():
    """Generate empty data"""
    yield {}

def missing_value_iteration(payload):
    """Generate all iterations of missing data"""
    for item in payload:
        yield {key : payload[key] for key in payload if item != key}

def custom_val_iteraton(payload, custom_val):
    """Generate all iterations of custom data"""
    for item in payload:
        result = payload.copy()
        result[item] = custom_val
        yield result

def missing_value_combos(payload):
    """Generate all combinations of missing data"""
    yield {}
    for count, _ in enumerate(payload):
        for key_combo in itertools.combinations(payload, count):
            bad_dict = {key: payload[key] for key in key_combo}
            yield bad_dict

def custom_val_combos(payload, custom_val):
    """Generate all combinations of custom data"""
    for count, _ in enumerate(payload):
        for key_combo in itertools.combinations(payload, count):
            result = payload.copy()
            for key in result:
                if key not in key_combo:
                    result[key] = custom_val
            yield result

###################################################################################################
# Make Requests
###################################################################################################

def rest_get(url, parameters):
    """Make a GET rest call to the specified URL with parameters"""
    LOG.debug("====== GET ====== :: URL : %s", url)
    response = requests.get(url, headers=JSON_HEADER, params=parameters)
    if response.status_code >= 500:
        LOG.error("=====GET===== URL :: %s", url)
        LOG.error("====== PARAMETERS :: %s", parameters)
        LOG.error("============= RESPONSE BODY :: %s", json.load_response_data(response))
    else:
        LOG.debug("=====GET===== URL :: %s", url)
        LOG.debug("====== PARAMETERS :: %s", parameters)
        LOG.debug("============= RESPONSE BODY :: %s", json.load_response_data(response))
    LOG.debug("==== RESPONSE RECIEVED ==== :: Status Code : %s", response.status_code)
    return response

def rest_post(url, parameters, payload):
    """Make a POST rest call to the specified URL and payload"""
    LOG.debug("====== POST ====== :: URL : %s", url)
    response = requests.post(url, headers=JSON_HEADER, params=parameters, json=payload)
    if response.status_code >= 500:
        LOG.error("=====POST==== URL :: %s", url)
        LOG.error("====== PARAMETERS :: %s", parameters)
        LOG.error("========= PAYLOAD :: %s", payload)
        LOG.error("============= RESPONSE BODY :: %s", json.load_response_data(response))
    else:
        LOG.debug("=====POST==== URL :: %s", url)
        LOG.debug("====== PARAMETERS :: %s", parameters)
        LOG.debug("========= PAYLOAD :: %s", payload)
        LOG.debug("============= RESPONSE BODY :: %s", json.load_response_data(response))
    LOG.debug("==== RESPONSE RECIEVED ==== :: Status Code : %s", response.status_code)
    return response

def rest_put(url, parameters, payload):
    """Make a PUT rest call to the specified URL and payload"""
    LOG.debug("====== PUT ====== :: URL : %s", url)
    response = requests.put(url, headers=JSON_HEADER, params=parameters, json=payload)
    if response.status_code >= 500:
        LOG.error("=====PUT===== URL :: %s", url)
        LOG.error("====== PARAMETERS :: %s", parameters)
        LOG.error("========= PAYLOAD :: %s", payload)
        LOG.error("============= RESPONSE BODY :: %s", json.load_response_data(response))
    else:
        LOG.debug("=====PUT===== URL :: %s", url)
        LOG.debug("====== PARAMETERS :: %s", parameters)
        LOG.debug("========= PAYLOAD :: %s", payload)
        LOG.debug("============= RESPONSE BODY :: %s", json.load_response_data(response))
    LOG.debug("==== RESPONSE RECIEVED ==== :: Status Code : %s", response.status_code)
    return response

def rest_patch(url, parameters, payload):
    """Make a PATCH rest call to the specified URL and payload"""
    LOG.debug("====== PATCH ====== :: URL : %s", url)
    response = requests.patch(url, headers=JSON_HEADER, params=parameters, json=payload)
    if response.status_code >= 500:
        LOG.error("====PATCH==== URL :: %s", url)
        LOG.error("====== PARAMETERS :: %s", parameters)
        LOG.error("========= PAYLOAD :: %s", payload)
        LOG.error("============= RESPONSE BODY :: %s", json.load_response_data(response))
    else:
        LOG.debug("====PATCH==== URL :: %s", url)
        LOG.debug("====== PARAMETERS :: %s", parameters)
        LOG.debug("========= PAYLOAD :: %s", payload)
        LOG.debug("============= RESPONSE BODY :: %s", json.load_response_data(response))
    LOG.debug("==== RESPONSE RECIEVED ==== :: Status Code : %s", response.status_code)
    return response

def rest_delete(url, parameters, payload):
    """Make a DELETE rest call to the specified URL and payload"""
    LOG.debug("====== DELETE ====== :: URL : %s", url)
    response = requests.delete(url, headers=JSON_HEADER, params=parameters, json=payload)
    if response.status_code >= 500:
        LOG.error("====DELETE==== URL :: %s", url)
        LOG.error("====== PARAMETERS :: %s", parameters)
        LOG.error("========= PAYLOAD :: %s", payload)
        LOG.error("============= RESPONSE BODY :: %s", json.load_response_data(response))
    else:
        LOG.debug("====DELETE==== URL :: %s", url)
        LOG.debug("====== PARAMETERS :: %s", parameters)
        LOG.debug("========= PAYLOAD :: %s", payload)
        LOG.debug("============= RESPONSE BODY :: %s", json.load_response_data(response))
    LOG.debug("==== RESPONSE RECIEVED ==== :: Status Code : %s", response.status_code)
    return response

def rest_call(action, url, parameters, payload):
    """Make the appropriate rest call base on the provided action"""
    action = str(action).upper()
    if action == 'GET':
        return rest_get(url, parameters)
    elif action == 'POST':
        return rest_post(url, parameters, payload)
    elif action == 'PUT':
        return rest_put(url, parameters, payload)
    elif action == 'PATCH':
        return rest_patch(url, parameters, payload)
    elif action == 'DELETE':
        return rest_delete(url, parameters, payload)
    else:
        LOG.error("Invalid Rest Call : %s", action)
        return rest_get(url, payload)
    