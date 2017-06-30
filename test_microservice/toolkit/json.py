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

LOG = logging.getLogger(__name__)

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

def load_endpoint_path(directory, endpoint):
    """Load url path at specified endpoint"""
    with open(directory) as stream:
        data = json.load(stream)
        path = data["services"][endpoint]["path"]
        LOG.debug("Loaded Path : %s", path)
        return path

def get_test_list(directory, endpoint):
    """Load list of all test payloads and expected results from endpoint"""
    with open(directory) as stream:
        data = json.load(stream)
        test_list = data["services"][endpoint]["test_data"]
        LOG.debug("Loaded test data : %s", test_list)
        return test_list

def load_test_data(directory, endpoint, index):
    """Load test description, payload, and expected results at index"""
    with open(directory) as stream:
        data = json.load(stream)
        base_payload = data["services"][endpoint]["test_data"][0][0]
        mod_payload = data["services"][endpoint]["test_data"][index][0]
        expected = data["services"][endpoint]["test_data"][index][1]
        description, payload = _build_payload(base_payload, mod_payload)
        LOG.debug("Loaded description : %s", description)
        LOG.debug("Loaded payload : %s", payload)
        LOG.debug("Loaded expected results : %s", expected)
        return description, payload, expected

def base_payload(directory, endpoint):
    """Load list of all test payloads and expected results from endpoint"""
    return load_test_payload(directory, endpoint, 0)

def load_test_payload(directory, endpoint, index):
    """Load expected data for specified endpoint and test"""
    with open(directory) as stream:
        data = json.load(stream)
        base_payload = data["services"][endpoint]["test_data"][0][0]
        mod_payload = data["services"][endpoint]["test_data"][index][0]
        description, payload = _build_payload(base_payload, mod_payload)
        LOG.debug("Loaded description : %s", description)
        LOG.debug("Loaded payload : %s", payload)
        return payload

def load_expected_response(directory, endpoint, index):
    """Load expected data for specified endpoint and test"""
    with open(directory) as stream:
        data = json.load(stream)
        expected = data["services"][endpoint]["test_data"][index][1]
        LOG.debug("Loaded expected data : %s", expected)
        return expected

def make_response_dict(response):
    """Return a dictionary of the response body"""
    response_dict = json.loads(response.text)
    LOG.debug("Made dictionary from response : %s", response_dict)
    return response_dict

def _build_payload(base_dict, mod_dict):
    """
    Assemble payload based on base payload and modificatons
    Ignore remove and test_description keys
    Anything specified in remove will be excluded from the payload
    """
    remove_list = []
    description = "No description provided"
    if "test_description" in mod_dict:
        description = mod_dict["test_description"]
    if "remove" in mod_dict:
        remove_list = mod_dict["remove"]
        LOG.debug("Keys to remove from base : %s", remove_list)
        if "all" in remove_list:
            base_dict = []
    built_dict = {key: mod_dict[key] for key in mod_dict
                  if key != "remove" and key != "test_description"}
    for key in base_dict:
        if key not in built_dict and key not in remove_list and key != "test_description":
            built_dict[key] = base_dict[key]
    LOG.debug("Assembled payload : %s", built_dict)
    return description, built_dict

def compare_response(response, exp_data):
    """
    Compare specified values in expected with those in response
    If status_code is specified, compare with response status code as well
    """
    exp_status_code = None
    if "status_code" in exp_data:
        exp_status_code = exp_data["status_code"]
    if exp_status_code:
        if response.status_code != exp_status_code:
            LOG.error("Bad response status code : %s Expected status code : %s",
                      response.status_code, exp_status_code)
            return False
    exp_response_dict = {key: exp_data[key] for key in exp_data if key != "status_code"}
    response_dict = make_response_dict(response)
    for key in exp_response_dict:
        if key in response_dict:
            if exp_response_dict[key] == response_dict[key]:
                continue
            else:
                LOG.error("Bad Response for %s :: Expected : %s Actual Response : %s",
                          key, exp_response_dict[key], response_dict[key])
                return False
        else:
            LOG.error("Bad Response :: Expected key : %s not contained in response", key)
            return False
    return True
