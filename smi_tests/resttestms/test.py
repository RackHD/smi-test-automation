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
import time
from . import json, http, log, parse

LOG = logging.getLogger(__name__)

###################################################################################################
# Test Initialization
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

def select_depth(default_depth, override):
    """Compare default depth and override to determine depth"""
    LOG.debug("Default depth :: %s Override :: %s", default_depth, override)
    depth = override if override else default_depth
    LOG.info("Selected depth was %s", depth)
    return int(depth)

###################################################################################################
# Premade Tests
###################################################################################################

@log.exception(LOG)
def delay(seconds=1):
    "Delay testing by specified number of seconds"
    LOG.info("%s second delay", seconds)
    print("{} second delay".format(seconds))
    time.sleep(seconds)

@log.exception(LOG)
def induce_error(action, end_class, missing_val=True, empty_str=True,
                 bad_str=False, neg_num=False, special_str=False, intense=False):
    """Run variations of request to attempt to induce an error"""
    test_info = "{}.induce_error".format(end_class.__class__.__name__)
    url = end_class.BASE_URL + json.get_base_path(end_class)
    print("\nRunning " + test_info)
    LOG.info("Running %s", test_info)
    if end_class.DEPTH < 2:
        request = http.rest_call(action, url, {}, {})
        end_class.assertTrue(has_all_status_codes(request, ["<500"]), ("Expected Response Code : <500 Actual : %s" % request.status_code))
    else:
        if end_class.DEPTH >= 3:
            intense = True
        for bad_param_generator in _bad_data_generators(json.get_base_parameters(end_class), missing_val, empty_str, bad_str, neg_num, special_str, intense):
            for bad_payload_generator in _bad_data_generators(json.get_base_payload(end_class), missing_val, empty_str, bad_str, neg_num, special_str, intense):
                test_failed = False
                for bad_param_combo in bad_param_generator:
                    for bad_payload_combo in bad_payload_generator:
                        if test_failed:
                            break
                        request = http.rest_call(action, url, bad_param_combo, bad_payload_combo)
                        with end_class.subTest(data=(str(bad_param_combo) + str(bad_payload_combo))):
                            try:
                                end_class.assertTrue(has_all_status_codes(request, ["<500"]), ("Expected Response Code : <500 Actual : %s" % request.status_code))
                            except AssertionError:
                                test_failed = True

# Deprecated for the time being, will be modified in the future
###############################################################
# @log.exception(LOG)
# def bad_data_except(action, end_class, good_params, good_payloads, missing_val=True, empty_str=True,
#                     bad_str=False, neg_num=False, special_str=False, intense=False):
#     """Run requests with missing or empty data excluding those specified, check for failure"""
#     test_info = "{}.bad_data with exceptions {} {}".format(end_class.__class__.__name__, good_params, good_payloads)
#     print("\nRunning " + test_info)
#     LOG.info("Running %s", test_info)
#     for param_combo in _bad_data_combos_except(json.get_base_parameters(end_class), good_params, missing_val, empty_str, bad_str, neg_num, special_str, intense):
#         for payload_combo in _bad_data_combos_except(json.get_base_payload(end_class), missing_val, empty_str, bad_str, neg_num, special_str, intense):
#             url = end_class.BASE_URL + json.get_base_path(end_class)
#             request = http.rest_call(action, url, param_combo, payload_combo)
#             with end_class.subTest(data=(str(param_combo) + str(payload_combo))):
#                 end_class.assertTrue(has_all_status_codes(request, ["400"]), ("Expected Response Code : 400 Actual : %s" % request.status_code))
###############################################################

@log.exception(LOG)
def run_mod_json_test(action, self_class, end_class, test_name, test_mods=None):
    """Run test specified in json with indicated modifications"""
    test_case = json.get_test_case(end_class, test_name)
    if test_mods:
        test_case = parse.combine_test_cases(test_case, test_mods)
    if test_case["skip"]:
        test_skip_info = "{}.{} : {} : {}".format(end_class.__class__.__name__, test_name, test_case["skip"], test_case["description"])
        print("Skipping " + test_skip_info)
        LOG.info("Skipping %s", test_skip_info)
        return None
    else:
        url = self_class.BASE_URL + test_case["path"]
        test_info = "{}.{} : {}".format(end_class.__class__.__name__, test_name, test_case["description"])
        print("Running " + test_info)
        LOG.info("Running %s", test_info)
        with self_class.subTest(test=test_info):
            request = http.rest_call(action, url, test_case["parameters"], test_case["payload"])
            self_class.assertTrue(compare_request(request, test_case["status_code"], test_case["response"]), test_case["error"])
            return json.load_response_data(request)

@log.exception(LOG)
def run_json_test(action, self_class, end_class, test_name):
    """Run a single test define in json file"""
    return run_mod_json_test(action, self_class, end_class, test_name)

@log.exception(LOG)
def auto_run_json_tests(action, end_class):
    """Run all tests in json for an endpoint"""
    LOG.info("Begin JSON defined %s tests for %s", str(action).upper(), end_class.__class__.__name__)
    print("")
    for test_name in json.get_all_tests(end_class):
        if json.check_auto_run(end_class, test_name):
            run_json_test(action, end_class, end_class, test_name)

###################################################################################################
# Test Data Generators
###################################################################################################

def _bad_data_generators(payload, missing_val=True, empty_str=True,
                     bad_str=False, neg_num=False, special_str=False, intense=False):
    """Output all generators for test data"""
    if intense or missing_val:
        yield http.missing_value_combos(payload)
    if intense or empty_str:
        yield http.custom_val_combos(payload, '')
    if intense or bad_str:
        yield http.custom_val_combos(payload, 'foobar007')
    if intense or neg_num:
        yield http.custom_val_combos(payload, -15)
    if intense or special_str:
        special_string = "\"\'\\!@#$%^&*()_-+=,./<>?{}[]|/0123456789~`\n\t\\\'\""
        yield http.custom_val_combos(payload, special_string)

# Deprecated for the time being, will be modified in the future
###############################################################
# def _bad_data_combos_except(payload, good_combos, missing_val=True, empty_str=True,
#                             bad_str=False, neg_num=False, special_str=False, intense=False):
#     """Generate all combinations of empty and missing data except for those specified"""
#     for bad_combo in _bad_data_combos(payload, missing_val, empty_str, bad_str, neg_num, special_str, intense):
#         valid_bad_combo = True
#         for good_combo in good_combos:
#             if set(good_combo) == set(bad_combo.keys()):
#                 valid_bad_combo = False
#         if valid_bad_combo:
#             yield bad_combo
###############################################################


###################################################################################################
# Test Results
###################################################################################################

def has_status_code(response, status_code):
    """Check if response status code is less than, greater than, or equal to specifed code"""
    return check_status_code(response.status_code, status_code)

def has_all_status_codes(response, status_codes):
    """Check if response status code is less than, greater than, or equal to specifed code"""
    return check_all_status_codes(response.status_code, status_codes)

def check_status_code(status_code, exp_status):
    """Check if provided status code is less than, greater than, or equal to specifed code"""
    negate, operation, exp_code = parse.status_code(exp_status)
    status_code, exp_code = int(status_code), int(exp_code)
    LOG.debug("Checking Response Status Code :: Expected : %s%s %s Actual : %s",
              "Not " if negate else "", operation, exp_code, status_code)
    is_good_code = False
    if operation == '=' or operation == '==':
        is_good_code = status_code == exp_code
    elif operation == '>':
        is_good_code = status_code > exp_code
    elif operation == '<':
        is_good_code = status_code < exp_code
    elif operation == '>=':
        is_good_code = status_code >= exp_code
    elif operation == '<=':
        is_good_code = status_code <= exp_code
    if negate:
        is_good_code = not is_good_code
    return is_good_code

def check_all_status_codes(status_code, status_code_list):
    """Check through list of status codes to make sure one is met"""
    all_codes_met = True
    for code in status_code_list:
        if not check_status_code(status_code, code):
            all_codes_met = False
    return all_codes_met

def compare_request(request, status_codes, exp_data):
    """
    Compare specified values in expected with those in response
    If status_code is specified, compare with response status code as well
    """
    if not check_all_status_codes(request.status_code, status_codes):
        LOG.error("============ BAD RESPONSE ============ :: Expected status code : %s Actual Status Code : %s",
                    status_codes, request.status_code)
        return False
    else:
        request_data = json.load_response_data(request)
        return contains_expected(request_data, exp_data)

def contains_expected(container, expected):
    """Recursively check container to make sure expected is contained within"""
    if expected == "KEY_PRESENT":
        return True
    if expected == "VALUE_PRESENT":
        return container != None
    if expected == "DATA_PRESENT":
        return len(container) > 0
    LOG.debug("Contains Expected :: Expected : %s Actual : %s", expected, container)
    if not isinstance(container, type(expected)):
        return False
    if isinstance(expected, (dict)):
        for item in expected:
            if item not in container:
                LOG.error("============ BAD RESPONSE ============ :: Expected key \"%s\" not contained in response", item)
                return False
            if not contains_expected(container[item], expected[item]):
                LOG.error("============ BAD RESPONSE ============ :: Key: %s Expected : %s Actual : %s",
                item, expected[item], container[item])
                return False
        return True
    if isinstance(expected, (list)):
        everything_found = True
        for item in expected:
            item_found = False
            for container_item in container:
                if _contains_expected_unlogged(container_item, item):
                    item_found = True
            if not item_found:
                LOG.error("============ BAD RESPONSE ============ :: Expected : %s not contained in Actual : %s",
                item, container)
                everything_found = False
        return everything_found
    else:
        return container == expected

def _contains_expected_unlogged(container, expected):
    """Recursively check container to make sure expected is contained within"""
    if expected == "KEY_PRESENT":
        return True
    if expected == "VALUE_PRESENT":
        return container != None
    if expected == "DATA_PRESENT":
        return len(container) > 0
    if not isinstance(container, type(expected)):
        return False
    if isinstance(expected, (dict)):
        for item in expected:
            if item not in container or not _contains_expected_unlogged(container[item], expected[item]):
                return False
        return True
    if isinstance(expected, (list)):
        everything_found = True
        for item in expected:
            item_found = False
            for container_item in container:
                if _contains_expected_unlogged(container_item, item):
                    item_found = True
            if not item_found:
                everything_found = False
        return everything_found
    else:
        return container == expected