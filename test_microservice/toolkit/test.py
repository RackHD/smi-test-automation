# -*- coding: utf-8 -*-
"""
Testing Toolkit
~~~~~~~~~~~~
Series of tools designed to control testing

:Copyright: (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
:License: Apache 2.0, see LICENSE for more details.
:Author: Akash Kwatra

Created on June 28, 2017
"""

import logging
from . import json,http

LOG = logging.getLogger(__name__)

def has_status_code(response, status):
    """Check if response status code is equal to specifed code"""
    LOG.debug("Response Status Code: %s", response.status_code)
    return response.status_code == status

def bad_parameter_combos(payload):
    """Generate all combinations of empty and missing parameters"""
    for empty_combo in http.empty_parameter_combos(payload):
        yield empty_combo
    for incomplete_combo in http.missing_parameter_combos(payload):
        yield incomplete_combo

def build_payload(base_dict, mod_dict):
    """
    Assemble payload based on base payload and modificatons
    Ignore remove and test_description keys
    Anything specified in remove will be excluded from the payload
    """
    remove_list = ["REMOVE", "DESCRIPTION", "SKIP"]
    description = "No description provided"
    skip = None
    built_dict = {key: mod_dict[key] for key in mod_dict
                  if key not in remove_list}
    if "SKIP" in mod_dict:
        skip = mod_dict["SKIP"]
    if "DESCRIPTION" in mod_dict:
        description = mod_dict["DESCRIPTION"]
    if "REMOVE" in mod_dict:
        remove_list.extend(mod_dict["REMOVE"])
        LOG.debug("Keys to remove from base : %s", remove_list)
        if "all" in remove_list:
            base_dict = []
    for key in base_dict:
        if key not in built_dict and key not in remove_list:
            built_dict[key] = base_dict[key]
    return skip, description, built_dict

def compare_response(response, exp_data):
    """
    Compare specified values in expected with those in response
    If status_code is specified, compare with response status code as well
    """
    exp_status_code = None
    if "STATUS_CODE" in exp_data:
        exp_status_code = exp_data["STATUS_CODE"]
    if exp_status_code:
        if response.status_code != exp_status_code:
            LOG.error("Bad response status code : %s Expected status code : %s",
                      response.status_code, exp_status_code)
            return False
    exp_response_dict = {key: exp_data[key] for key in exp_data if key != "STATUS_CODE"}
    response_dict = json.make_response_dict(response)
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
