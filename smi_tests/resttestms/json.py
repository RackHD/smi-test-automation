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

###################################################################################################
# Class Test Loaders
###################################################################################################

def check_auto_run(end_class, test_name):
    """Check to see if specified test should be auto run"""
    return endpoint_check_auto_run(end_class.JSON_FILE, end_class.ENDPOINT, test_name)

def get_all_tests(end_class):
    """Load list of all test cases from class"""
    return endpoint_load_all_tests(end_class.JSON_FILE, end_class.ENDPOINT)

def get_test_case(end_class, test_name):
    """Load specific test case from an endpoint"""
    return endpoint_load_test_case(end_class.JSON_FILE, end_class.ENDPOINT, test_name)

def get_base_path(end_class):
    """Load base path in class for specified class"""
    return endpoint_load_base_path(end_class.JSON_FILE, end_class.ENDPOINT)

def get_test_path(end_class, test_name):
    """Load path in class for specified test"""
    return endpoint_load_test_path(end_class.JSON_FILE, end_class.ENDPOINT, test_name)

def get_base_parameters(end_class):
    """Load base parameters in class for specified class"""
    return endpoint_load_base_parameters(end_class.JSON_FILE, end_class.ENDPOINT)

def get_test_parameters(end_class, test_name):
    """Load parameters in class for specified test"""
    return endpoint_load_test_parameters(end_class.JSON_FILE, end_class.ENDPOINT, test_name)

def get_base_payload(end_class):
    """Load base payload in class for specified class"""
    return endpoint_load_base_payload(end_class.JSON_FILE, end_class.ENDPOINT)

def get_test_payload(end_class, test_name):
    """Load payload in class for specified test"""
    return endpoint_load_test_payload(end_class.JSON_FILE, end_class.ENDPOINT, test_name)

def get_base_status_codes(end_class):
    """Load base status code in class for specified class"""
    return endpoint_load_base_status_codes(end_class.JSON_FILE, end_class.ENDPOINT)

def get_test_status_codes(end_class, test_name):
    """Load expected data from class for specified test"""
    return endpoint_load_test_status_codes(end_class.JSON_FILE, end_class.ENDPOINT, test_name)

def get_base_response(end_class):
    """Load base response in class for specified class"""
    return endpoint_load_base_response(end_class.JSON_FILE, end_class.ENDPOINT)

def get_test_response(end_class, test_name):
    """Load expected data from class for specified test"""
    return endpoint_load_test_response(end_class.JSON_FILE, end_class.ENDPOINT, test_name)

###################################################################################################
# General Test Loaders
###################################################################################################

def endpoint_check_auto_run(directory, endpoint, test_name):
    """Check to see if specified test at endpoint should be auto run"""
    with open(directory) as stream:
        data = json.load(stream)
        test_data = data[endpoint]
        auto_run = parse.build_test_case(test_data, test_name)["auto_run"]
        return auto_run

def endpoint_load_all_tests(directory, endpoint):
    """Load list of all test cases from an endpoint"""
    with open(directory) as stream:
        data = json.load(stream)
        test_dict = data[endpoint]
        LOG.debug("Loaded test data : %s", test_dict)
        return test_dict

def endpoint_load_test_case(directory, endpoint, test_name):
    """Load test description, payload, and expected results at index"""
    with open(directory) as stream:
        data = json.load(stream)
        test_data = data[endpoint]
        return parse.build_test_case(test_data, test_name)

def endpoint_load_base_path(directory, endpoint):
    """Load base path from endpoint"""
    return endpoint_load_test_path(directory, endpoint, BASE)

def endpoint_load_test_path(directory, endpoint, test_name):
    """Load expected path for specified endpoint and test"""
    with open(directory) as stream:
        data = json.load(stream)
        test_data = data[endpoint]
        path = parse.build_test_case(test_data, test_name)["path"]
        return path

def endpoint_load_base_parameters(directory, endpoint):
    """Load base parameters from endpoint"""
    return endpoint_load_test_parameters(directory, endpoint, BASE)

def endpoint_load_test_parameters(directory, endpoint, test_name):
    """Load expected parameters for specified endpoint and test"""
    with open(directory) as stream:
        data = json.load(stream)
        test_data = data[endpoint]
        parameters = parse.build_test_case(test_data, test_name)["parameters"]
        return parameters

def endpoint_load_base_payload(directory, endpoint):
    """Load base payload from endpoint"""
    return endpoint_load_test_payload(directory, endpoint, BASE)

def endpoint_load_test_payload(directory, endpoint, test_name):
    """Load expected payload for specified endpoint and test"""
    with open(directory) as stream:
        data = json.load(stream)
        test_data = data[endpoint]
        payload = parse.build_test_case(test_data, test_name)["payload"]
        return payload

def endpoint_load_base_status_codes(directory, endpoint):
    """Load base status_code from endpoint"""
    return endpoint_load_test_status_codes(directory, endpoint, BASE)

def endpoint_load_test_status_codes(directory, endpoint, test_name):
    """Load expected status code for specified endpoint and test"""
    with open(directory) as stream:
        data = json.load(stream)
        test_data = data[endpoint]
        status_codes = parse.build_test_case(test_data, test_name)["status_code"]
        return status_codes

def endpoint_load_base_response(directory, endpoint):
    """Load base response from endpoint"""
    return endpoint_load_test_response(directory, endpoint, BASE)

def endpoint_load_test_response(directory, endpoint, test_name):
    """Load expected response for specified endpoint and test"""
    with open(directory) as stream:
        data = json.load(stream)
        test_data = data[endpoint]
        response = parse.build_test_case(test_data, test_name)["response"]
        return response

###################################################################################################
# JSON Utilites
###################################################################################################

def load_response_data(response):
    """Return the data of the response body"""
    try:
        response_data = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        response_data = {}
    return response_data
