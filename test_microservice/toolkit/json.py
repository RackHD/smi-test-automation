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

def load_inital_test_data(directory, endpoint):
    """Load initial test data from provided json file"""
    with open(directory) as stream:
        data = json.load(stream)
        path = data["services"][endpoint]["path"]
        parameters = data["services"][endpoint]["parameters"][0]
        payload = data["services"][endpoint]["payload"][0]
        return path, parameters, payload

def load_test_path(directory, endpoint):
    """Load url path at specified endpoint"""
    with open(directory) as stream:
        data = json.load(stream)
        path = data["services"][endpoint]["path"]
        return path

def load_test_parameters(directory, endpoint, index):
    """Load modified paramters at specified endpoint and index"""
    with open(directory) as stream:
        data = json.load(stream)
        base_parameters = data["services"][endpoint]["parameters"][0]
        mod_parameters = data["services"][endpoint]["parameters"][index]
        return _combine_dictionaries(base_parameters, mod_parameters)

def load_test_payload(directory, endpoint, index):
    """Load modified payload at specified endpoint and index"""
    with open(directory) as stream:
        data = json.load(stream)
        base_payload = data["services"][endpoint]["parameters"][0]
        mod_payload = data["services"][endpoint]["parameters"][index]
        return _combine_dictionaries(base_payload, mod_payload)

def _combine_dictionaries(base_dict, mod_dict):
    """
    Compare base dictionary with modifications
    Modify all values specified in modificaton dictionary
    Use base dictionary for all unspecified values
    If remove key is used, remove all keys associated with remove
    If remove is passed all, ignore base dictionary
    """
    remove_list = []
    if "remove" in mod_dict:
        remove_list = mod_dict["remove"]
        if "all" in remove_list:
            return mod_dict
    combined_dict = {}
    for key in base_dict:
        if key not in remove_list:
            if key in mod_dict:
                combined_dict[key] = mod_dict[key]
            else:
                combined_dict[key] = base_dict[key]
    return combined_dict
