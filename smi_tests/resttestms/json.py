# -*- coding: utf-8 -*-
"""
JSON Toolkit
~~~~~~~~~~~~
Series of tools designed around using JSON files

:Copyright: (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
:License: Apache 2.0, see LICENSE for more details.
:Author: Akash Kwatra

Created on June 26, 2017
"""

import logging
import json
from . import parse

LOG = logging.getLogger(__name__)

BASE = 'test_base'

###################################################################################################
# Initialize Class Data
###################################################################################################

def select_directory(default_directory, override):
    """Compare default directory and override to determine json directory"""
    LOG.debug("Default Directory :: %s Override :: %s", default_directory, override)
    directory = override if override else default_directory
    LOG.info("Selected data directory was %s", directory)
    return directory

def create_json_reference(directory, filename):
    """Use the directory and filename, generate a json reference"""
    LOG.debug("Provided Directory: %s JSON File: %s", directory, filename)
    json_reference = "{}/{}".format(directory, filename)
    LOG.debug("Generated Reference :: %s", json_reference)
    return json_reference

def endpoint_load_path(directory, endpoint):
    """Load url path at specified endpoint"""
    with open(directory) as stream:
        data = json.load(stream)
        path = data[endpoint]["path"]
        LOG.debug("Loaded Path : %s", path)
        return path

###################################################################################################
# Class Test Loaders
###################################################################################################

def get_path(end_class):
    """Load url path at for specified class"""
    return endpoint_load_path(end_class.JSON_FILE, end_class.ENDPOINT)

def get_all_tests(end_class):
    """Load list of all test payloads and expected results from class"""
    return endpoint_load_all_tests(end_class.JSON_FILE, end_class.ENDPOINT)

def get_test(end_class, test_name):
    """Load test description, payload, and expected results from class at index"""
    return endpoint_load_test(end_class.JSON_FILE, end_class.ENDPOINT, test_name)

def get_base_payload(end_class):
    """Load base payload in class for specified class"""
    return endpoint_load_base_payload(end_class.JSON_FILE, end_class.ENDPOINT)

def get_test_payload(end_class, test_name):
    """Load payload in class for specified test"""
    return endpoint_load_test_payload(end_class.JSON_FILE, end_class.ENDPOINT, test_name)

def get_base_payload(end_class):
    """Load base status code in class for specified class"""
    return endpoint_load_base_status_code(end_class.JSON_FILE, end_class.ENDPOINT)

def get_test_status_code(end_class, test_name):
    """Load expected data from class for specified test"""
    return endpoint_load_test_status_code(end_class.JSON_FILE, end_class.ENDPOINT, test_name)

def get_base_response(end_class):
    """Load base response in class for specified class"""
    return endpoint_load_base_response(end_class.JSON_FILE, end_class.ENDPOINT)

def get_test_response(end_class, test_name):
    """Load expected data from class for specified test"""
    return endpoint_load_test_response(end_class.JSON_FILE, end_class.ENDPOINT, test_name)

###################################################################################################
# General Test Loaders
###################################################################################################

def endpoint_load_all_tests(directory, endpoint):
    """Load list of all test payloads and expected results from endpoint"""
    with open(directory) as stream:
        data = json.load(stream)
        test_dict = data[endpoint]["test_data"]
        LOG.debug("Loaded test data : %s", test_dict)
        return test_dict

def endpoint_load_test(directory, endpoint, test_name):
    """Load test description, payload, and expected results at index"""
    with open(directory) as stream:
        data = json.load(stream)
        test_data = data[endpoint]["test_data"]
        return parse.build_test_case(test_data, test_name)

def endpoint_load_base_payload(directory, endpoint):
    """Load base payload from endpoint"""
    return endpoint_load_test_payload(directory, endpoint, BASE)

def endpoint_load_test_payload(directory, endpoint, test_name):
    """Load expected payload for specified endpoint and test"""
    with open(directory) as stream:
        data = json.load(stream)
        test_data = data[endpoint]["test_data"]
        _, _, payload, _, _, _ = parse.build_test_case(test_data, test_name)
        return payload

def endpoint_load_base_status_codes(directory, endpoint):
    """Load base status_code from endpoint"""
    return endpoint_load_test_status_codes(directory, endpoint, BASE)

def endpoint_load_test_status_codes(directory, endpoint, test_name):
    """Load expected status code for specified endpoint and test"""
    with open(directory) as stream:
        data = json.load(stream)
        test_data = data[endpoint]["test_data"]
        _, _, _, status_codes, _, _ = parse.build_test_case(test_data, test_name)
        return status_codes

def endpoint_load_base_response(directory, endpoint):
    """Load base response from endpoint"""
    return endpoint_load_test_response(directory, endpoint, BASE)

def endpoint_load_test_response(directory, endpoint, test_name):
    """Load expected response for specified endpoint and test"""
    with open(directory) as stream:
        data = json.load(stream)
        test_data = data[endpoint]["test_data"]
        _, _, _, _, response, _ = parse.build_test_case(test_data, test_name)
        return response

###################################################################################################
# JSON Utilites
###################################################################################################

def load_response_data(response):
    """Return the data of the response body"""
    response_data = json.loads(response.text)
    LOG.debug("Loading data from response : %s", response_data)
    return response_data
