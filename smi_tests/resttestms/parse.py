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
    host = re.sub("host:", "", str(arg).lower())
    return host

def is_data(arg):
    """Check to see if provided argument is a data directory"""
    data = False
    if re.search(r'data:|/|\.\.', str(arg).lower()):
        data = True
    return data

def get_data(arg):
    """Get data directory from provided argument"""
    data = re.sub("data:", "", str(arg).lower())
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
        skip = "TEST SKIPPED :: " + mod_dict["SKIP"]
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
