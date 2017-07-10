# -*- coding: utf-8 -*-
"""
Test Toolkit
~~~~~~~~~~~~
Series of tools designed to control testing

:Copyright: (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
:License: Apache 2.0, see LICENSE for more details.
:Author: Akash Kwatra

Created on June 28, 2017
"""

import logging
from . import json, http, log, parse

LOG = logging.getLogger(__name__)

###################################################################################################
# Premade Tests
###################################################################################################

@log.exception(LOG)
def get_bad_data(end_class):
    """Run GET requests with missing or empty data, check for failure"""
    LOG.info("Begin GET tests for %s using bad data", end_class.__class__.__name__)
    for combo in _bad_data_combos(json.get_base_payload(end_class)):
        response = http.rest_get(end_class.URL, combo)
        with end_class.subTest(data=combo):
            end_class.assertTrue(has_status_code(response, "<= 400"), "Expected Response Code : 400")

@log.exception(LOG)
def post_bad_data(end_class):
    """Run POST requests with missing or empty data, check for failure"""
    LOG.info("Begin POST tests for %s using bad data", end_class.__class__.__name__)
    for combo in _bad_data_combos(json.get_base_payload(end_class)):
        response = http.rest_post(end_class.URL, combo)
        with end_class.subTest(data=combo):
            end_class.assertTrue(has_status_code(response, "<= 400"), "Expected Response Code : 400")

@log.exception(LOG)
def get_bad_data_except(end_class, good_combos):
    """Run GET requests with missing or empty data excluding those specified, check for failure"""
    LOG.info("Begin GET tests for %s using bad data with the following exceptions :: %s",
             end_class.__class__.__name__, good_combos)
    for combo in _bad_data_combos_except(json.get_base_payload(end_class), good_combos):
        response = http.rest_get(end_class.URL, combo)
        with end_class.subTest(data=combo):
            end_class.assertTrue(has_status_code(response, "<= 400"), "Expected Response Code : 400")

@log.exception(LOG)
def post_bad_data_except(end_class, good_combos):
    """Run POST requests with missing or empty data excluding those specified, check for failure"""
    LOG.info("Begin POST tests for %s using bad data with the following exceptions :: %s",
             end_class.__class__.__name__, good_combos)
    for combo in _bad_data_combos_except(json.get_base_payload(end_class), good_combos):
        response = http.rest_post(end_class.URL, combo)
        with end_class.subTest(data=combo):
            end_class.assertTrue(has_status_code(response, ">= 400"), "Expected Response Code : 400")

@log.exception(LOG)
def get_json(end_class):
    """Run tests specified in JSON using GET requests"""
    LOG.info("Begin JSON defined GET tests for %s", end_class.__class__.__name__)
    print("")
    for test_case in json.get_all_tests(end_class):
        skip, description, payload, expected = json.parse_test(end_class, test_case)
        if skip:
            print(skip)
        else:
            response = http.rest_get(end_class.URL, payload)
            with end_class.subTest(test=description):
                end_class.assertTrue(compare_response(response, expected), "Bad Response")

@log.exception(LOG)
def post_json(end_class):
    """Run tests specified in JSON using POST requests"""
    LOG.info("Begin JSON defined POST tests for %s", end_class.__class__.__name__)
    print("")
    for test_case in json.get_all_tests(end_class):
        skip, description, payload, expected = json.parse_test(end_class, test_case)
        if skip:
            print(skip)
        else:
            response = http.rest_post(end_class.URL, payload)
            with end_class.subTest(test=description):
                end_class.assertTrue(compare_response(response, expected), "Bad Response")

###################################################################################################
# Test Data Generators
###################################################################################################

def _bad_data_combos(payload):
    """Generate all combinations of empty and missing data"""
    for empty_combo in http.empty_data_combos(payload):
        yield empty_combo
    for incomplete_combo in http.missing_data_combos(payload):
        yield incomplete_combo

def _bad_data_combos_except(payload, good_combos):
    """Generate all combinations of empty and missing data except for those specified"""
    for bad_combo in _bad_data_combos(payload):
        valid_bad_combo = True
        for good_combo in good_combos:
            if set(good_combo) == set(bad_combo.keys()):
                valid_bad_combo = False
        if valid_bad_combo:
            yield bad_combo

###################################################################################################
# Test Results
###################################################################################################

def has_status_code(response, status_code):
    """Check if response status code is less than, greater than, or equal to specifed code"""
    check_status_code(response.status_code, status_code)

def check_status_code(status_code, exp_status):
    """Check if provided status code is less than, greater than, or equal to specifed code"""
    operation, exp_code = parse.status_code(exp_status)
    status_code, exp_code = int(status_code), int(exp_code)
    LOG.debug("Checking Response Status Code :: Expected : %s %s Actual : %s", operation, exp_code, status_code)
    if operation == '=' or operation == '==':
        return status_code == exp_code
    elif operation == '>':
        return status_code > exp_code
    elif operation == '<':
        return status_code < exp_code
    elif operation == '>=':
        return status_code >= exp_code
    elif operation == '<=':
        return status_code <= exp_code

def compare_response(response, exp_data):
    """
    Compare specified values in expected with those in response
    If status_code is specified, compare with response status code as well
    """
    response_dict = json.make_response_dict(response)
    return compare_data(response.status_code, response_dict, exp_data)

def compare_data(status_code, response_dict, exp_data):
    """
    Compare specified values in expected with those in response dictionary
    If status_code is specified, compare with response status code as well
    """
    exp_status_code = None
    if "STATUS_CODE" in exp_data:
        exp_status_code = exp_data["STATUS_CODE"]
    if exp_status_code:
        if not check_status_code(status_code, exp_status_code):
            LOG.error("============ BAD RESPONSE ============ :: Expected status code : %s Actual Status Code : %s",
                      exp_status_code, status_code)
            return False
    exp_response_dict = {key: exp_data[key] for key in exp_data if key != "STATUS_CODE"}
    return recursive_equal(response_dict, exp_response_dict)

def recursive_equal(response, expected):
    """Recursively compare iterable data to check for equality"""
    if not isinstance(expected, type(response)):
        return False
    if isinstance(expected, (dict)):
        for item in expected:
            if item not in response:
                LOG.error("============ BAD RESPONSE ============ :: Expected key \"%s\" not contained in response", item)
                return False
            if not recursive_equal(response[item], expected[item]):
                LOG.error("============ BAD RESPONSE ============ :: Key: %s Expected : %s Actual : %s",
                        item, response[item], expected[item])
                return False
        return True
    if isinstance(expected, (list, tuple, set)):
        for exp_item in expected:
            found = False
            for resp_item in response:
                if(recursive_equal(resp_item, exp_item)):
                    found = True
            if not found:
                LOG.error("============ BAD RESPONSE ============ :: Expected key \"%s\" not contained in response", exp_item)
                return False
        return True
    else:
        return response == expected