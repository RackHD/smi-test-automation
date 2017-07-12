# -*- coding: utf-8 -*-
"""
Parse Toolkit
~~~~~~~~~~~~~
Series of tools designed to parse data

:Copyright: (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
:License: Apache 2.0, see LICENSE for more details.
:Author: Akash Kwatra

Created on July 6, 2017
"""

import logging
import re

LOG = logging.getLogger(__name__)

BASE = 'test_base'

###################################################################################################
# Special Argument Parsers
###################################################################################################

def is_host(arg):
    """Check to see if provided argument is a host"""
    host = False
    if re.search(r'localhost|host:|.+\..*', str(arg).lower()):
        host = True
    return host

def get_host(arg):
    """Get host from provided argument"""
    host = re.sub(r'host:', "", str(arg).lower())
    return host

def is_data(arg):
    """Check to see if provided argument is a data directory"""
    data = False
    if re.search(r'data:|/|\.\.', str(arg).lower()):
        data = True
    return data

def get_data(arg):
    """Get data directory from provided argument"""
    data = re.sub(r'data:', "", str(arg).lower())
    return data

def has_negate(arg):
    """Check to see if provided argument contains negation flags"""
    negate = False
    if re.search("[\\^\\!]", str(arg)):
        negate = True
    return negate

def strip_negate(arg):
    """Strip argument of its negation flags"""
    stripped = re.sub("[\\^\\!]", "", str(arg))
    return stripped

###################################################################################################
# Test Data Parsers
###################################################################################################

def status_code(status):
    """Parse status code to get operation and code value"""
    operation = '='
    code = None
    if re.search(r'[=<>]', str(status)):
        operation = re.sub(r'[\d\s]', "", str(status))
    if re.search(r'[\d]', str(status)):
        code = int(re.sub(r'[=<>\s]', "", str(status)))
    return operation, code

def build_test_case(test_data, test_name):
    """Parse out all test case information using provided test data"""
    skip = None
    description = "No Description"
    error = "Bad Response"
    status_code = '200'
    payload, response = {}, {}
    if "skip" in test_data[test_name]:
        skip = test_data[test_name]["skip"]
    if "description" in test_data[test_name]:
        description = test_data[test_name]["description"]
    if "error" in test_data[test_name]:
        error = test_data[test_name]["error"]
    if "status_code" in test_data[test_name]:
        status_code = test_data[test_name]["status_code"]
    if "payload" in test_data[test_name]:
        mod_payload = test_data[test_name]["payload"]
        try:
            base_payload = test_data[BASE]["payload"]
        except KeyError:
            base_payload = mod_payload
            LOG.info("No base test data found for %s", test_name)
        payload = build_payload(base_payload, mod_payload)
    if "response" in test_data[test_name]:
        mod_response = test_data[test_name]["response"]
        try:
            base_response = test_data[BASE]["response"]
        except KeyError:
            base_response = mod_response
            LOG.info("No base test data found for %s", test_name)
        response = build_response(base_response, mod_response)
    if skip:
        LOG.debug("Skip this test")
    LOG.debug("Description : %s", description)
    LOG.debug("Payload : %s", payload)
    LOG.debug("Expected status code : %s", status_code)
    LOG.debug("Expected response : %s", response)
    LOG.debug("Error Message : %s", error)
    return skip, description, payload, status_code, response, error

def is_list_mod(potential_mod_string):
    "Check if list element is a modifier string"
    list_mod = False
    if re.search(r'REMOVE\s*:\s*|COMBINE\s*:\s*|REPLACE\s*:|INSERT\s*:\s*|APPEND\s*:?\s*', str(potential_mod_string)):
        list_mod = True
    return list_mod

def get_list_mod(mod_string):
    """Extract the list modification and arguments from a list modification string"""
    if "APPEND" in mod_string:
        return "APPEND", None
    else:
        spaceless_string = re.sub(r'\s', "", str(mod_string))
        mod_list = re.split(r':', spaceless_string)
        operation = mod_list[0]
        if operation == 'REMOVE' and 'all' in mod_list[1].lower():
            locations = 'all'
        else:
            locations = re.split(r',', mod_list[1])
            for index, location in enumerate(locations):
                if re.search(r'\d-\d', str(location)):
                    index_range = re.split(r'-', str(location))
                    index_start, index_finish = int(index_range[0]), int(index_range[1])
                    del locations[index]
                    locations[index:index] = [str(i) for i in range(index_start, index_finish)]
            locations = [int(i) for i in locations]
        return operation, locations

def build_payload(base_payload, mod_payload):
    """Construct test payload using base payload and modifications"""
    return _combine_items(base_payload, mod_payload)

def build_response(base_response, mod_response):
    """Construct test expected respose using base response and modifications"""
    return _combine_items(base_response, mod_response)

def _combine_items(base_item, mod_item):
    """Recursive utility to assemble items using the base and modifications"""
    if base_item == mod_item:
        return mod_item
    elif base_item and isinstance(mod_item, (dict)):
        base_dict, mod_dict = base_item, mod_item
        remove_list = ["REMOVE"]
        if "REMOVE" in mod_dict:
            remove_list.extend(mod_dict["REMOVE"])
            if "all" in remove_list:
                del mod_dict["REMOVE"]
                return mod_dict
        combined_dict = {key: base_dict[key] for key in base_dict if key not in remove_list}
        for key in mod_dict:
            if key not in remove_list:
                if key in combined_dict:
                    combined_dict[key] = _combine_items(combined_dict[key], mod_dict[key])
                else:
                    combined_dict[key] = mod_dict[key]
        return combined_dict
    elif base_item and isinstance(mod_item, (list)):
        base_list, mod_list = base_item, mod_item
        combined_list = base_list
        mod_args = None
        mod_mode = 'APPEND'
        combine, replace, insert = {}, {}, {}
        for item in mod_list:
            if is_list_mod(item):
                mod_mode, mod_args = get_list_mod(item)
                if mod_mode == 'REMOVE':
                    if mod_args == 'all':
                        combined_list = []
                    else:
                        for index in sorted(mod_args, reverse=True):
                            del combined_list[index]
                    mod_mode == 'APPEND'
            else:
                if mod_mode == 'COMBINE' and mod_args:
                    index = mod_args.pop(0)
                    combine[index] = item
                elif mod_mode == 'REPLACE' and mod_args:
                    index = mod_args.pop(0)
                    replace[index] = item
                elif mod_mode == 'INSERT' and mod_args:
                    index = mod_args.pop(0)
                    insert[index] = item
                else:
                    combined_list.append(item)
        for index in sorted(combine.keys(), reverse=True):
            combined_list[index] = _combine_items(combined_list[index], combine[index])
        for index in sorted(replace.keys(), reverse=True):
            combined_list[index] = replace[index]
        for index in sorted(insert.keys(), reverse=True):
            combined_list.insert(index, insert[index])
        return combined_list
    else:
        return mod_item

###################################################################################################
# System argument parsers
###################################################################################################

def single_microservice_args(sys_args):
    """Parse arguments when running a single microservice"""
    host_override = None
    data_override = None
    args = sys_args[1:]
    for arg in args:
        if is_host(arg):
            sys_args.remove(arg)
            host_override = get_host(arg)
            LOG.debug("Found Host : %s", host_override)
        elif is_data(arg):
            sys_args.remove(arg)
            data_override = get_data(arg)
            LOG.debug("Found Data : %s", data_override)
    return host_override, data_override

def auto_test_args(data_m_id, data_alias, *args):
    """Parse arguments from auto_tester to determine which tests will be loaded"""
    arguments = [arg for arg in args]
    test_keys = set()
    remove_keys = set()
    test_arguments = []
    remove_arguments = []
    host = None
    data = None
    if arguments:
        # Parse out special arguments
        for arg in arguments:
            if is_host(arg):
                host = get_host(arg)
            elif is_data(arg):
                data = get_data(arg)
            elif has_negate(arg):
                remove_arguments.append(strip_negate(arg))
            else:
                test_arguments.append(arg)
    # Default run all tests
    if not test_arguments:
        test_arguments = {val for val in data_alias.values()}

    def _add_arguments_to_set(set_arguments, target_set):
        """ Take in arguments with special parameters removed and add to target set """
        def _add_key_from_m_id(m_id_string):
            for m_id in str(m_id_string):
                if m_id in data_m_id:
                    target_set.add(m_id)
                else:
                    raise ValueError('Invalid Microservice ID - {} from {}'.format(m_id, m_id_string))

        def _add_key_from_alias(alias):
            alias = alias.upper()
            if alias in data_alias:
                target_set.add(data_alias[alias])
            else:
                raise ValueError('Invalid Microservice Alias - {}'.format(alias))

        for arg in set_arguments:
            if str(arg).upper() in data_alias:
                _add_key_from_alias(arg)
            elif str(arg).isalnum():
                _add_key_from_m_id(arg)
            else:
                raise ValueError('Invalid Argument - {}'.format(str(arg)))

    _add_arguments_to_set(remove_arguments, remove_keys)
    _add_arguments_to_set(test_arguments, test_keys)
    return host, data, (test_keys - remove_keys)
