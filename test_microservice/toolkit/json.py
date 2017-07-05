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
from . import test

LOG = logging.getLogger(__name__)

###################################################################################################
# Initialize Class Data
###################################################################################################

def select_directory(default_directory, override):
    """Compare default directory and override to determine json directory"""
    LOG.debug("Default Directory :: %s Override :: %s", default_directory, override)
    directory = override if override else default_directory
    LOG.info("Selected host was %s", directory)
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
        path = data["endpoints"][endpoint]["path"]
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

def parse_test(end_class, test_data):
    """Parse test description, payload, and expected results from test data"""
    base_payload = get_base_payload(end_class)
    mod_payload, expected = test_data[0], test_data[1]
    skip, description, payload = test.build_payload(base_payload, mod_payload)
    if skip:
        LOG.debug("Skip this test")
    LOG.debug("Description : %s", description)
    LOG.debug("Payload : %s", payload)
    LOG.debug("Expected results : %s", expected)
    return skip, description, payload, expected

def get_test(end_class, index):
    """Load test description, payload, and expected results from class at index"""
    return endpoint_load_test(end_class.JSON_FILE, end_class.ENDPOINT, index)

def get_base_payload(end_class):
    """Load base payload in class for specified class"""
    return endpoint_load_base_payload(end_class.JSON_FILE, end_class.ENDPOINT)

def get_test_payload(end_class, index):
    """Load payload in class for specified test"""
    return endpoint_load_test_payload(end_class.JSON_FILE, end_class.ENDPOINT, index)

def get_test_response(end_class, index):
    """Load expected data from class for specified test"""
    return endpoint_load_test_response(end_class.JSON_FILE, end_class.ENDPOINT, index)

###################################################################################################
# General Test Loaders
###################################################################################################

def endpoint_load_all_tests(directory, endpoint):
    """Load list of all test payloads and expected results from endpoint"""
    with open(directory) as stream:
        data = json.load(stream)
        test_list = data["endpoints"][endpoint]["test_data"]
        LOG.debug("Loaded test data : %s", test_list)
        return test_list

def endpoint_load_test(directory, endpoint, index):
    """Load test description, payload, and expected results at index"""
    with open(directory) as stream:
        data = json.load(stream)
        base_payload = data["endpoints"][endpoint]["test_data"][0][0]
        mod_payload = data["endpoints"][endpoint]["test_data"][index][0]
        expected = data["endpoints"][endpoint]["test_data"][index][1]
        skip, description, payload = test.build_payload(base_payload, mod_payload)
        if skip:
            LOG.debug("Skip this test")
        LOG.debug("Description : %s", description)
        LOG.debug("Payload : %s", payload)
        LOG.debug("Expected results : %s", expected)
        return skip, description, payload, expected

def endpoint_load_base_payload(directory, endpoint):
    """Load list of all test payloads and expected results from endpoint"""
    return endpoint_load_test_payload(directory, endpoint, 0)

def endpoint_load_test_payload(directory, endpoint, index):
    """Load expected data for specified endpoint and test"""
    with open(directory) as stream:
        data = json.load(stream)
        base_payload = data["endpoints"][endpoint]["test_data"][0][0]
        mod_payload = data["endpoints"][endpoint]["test_data"][index][0]
        payload = test.build_payload(base_payload, mod_payload)[2]
        if index != 0:
            LOG.debug("Loaded payload at index %s: %s", index, payload)
        return payload

def endpoint_load_test_response(directory, endpoint, index):
    """Load expected data for specified endpoint and test"""
    with open(directory) as stream:
        data = json.load(stream)
        expected = data["endpoints"][endpoint]["test_data"][index][1]
        LOG.debug("Loaded expected data at index %s: %s", index, expected)
        return expected

###################################################################################################
# JSON Utilites
###################################################################################################

def make_response_dict(response):
    """Return a dictionary of the response body"""
    response_dict = json.loads(response.text)
    LOG.debug("Made dictionary from response : %s", response_dict)
    return response_dict
