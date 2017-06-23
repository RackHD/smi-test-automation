# -*- coding: utf-8 -*-

#   __      ___  ___ _  __ ___          ___ _           ___ ___  _
#  (_  |\/|  | __ | |_ (_   | __ /\  | | | / \ |\/|  /\  |   |  / \ |\ |
#  __) |  | _|_   | |_ __)  |   /--\ |_| | \_/ |  | /--\ |  _|_ \_/ | \|

'''
SMI-TEST-AUTOMATION
~~~~~~~~~~~~~~~~~~~

Run specified microservice tests on specified host.
Tests run in no particular order.

-- Structure --
The default host is 'localhost'
Each microservice is assigned a 1 character ID
Each microservice ID is associated with an alias

-- Reference (ID:ALIAS) --
1:DISC 2:CHIN 3:SVIN 4:PWTH 5:SCP 6:VID 7:VNW 8:FWUP

-- Input --
Enter an IP address to assign it as host [100.68.125.170]
Use the prefix 'host:' to set a named host [host:node-example]
If no tests are specified, all will run by default
Microservice IDs can be separated with or without a space [123 or 1 2 3]
Microservice Aliases are case insensitive [DISC or disc]
Use the modifier '^' or '!' to skip a test
Host, Aliases, and IDs can be passed as parameters in any order
[host:node-example CHIN svin 1 56 !2]

Argument format examples:

>>> test_manager - Run all tests
>>> test_manager 4 - Run test with ID 4
>>> test_manager 7451725 - Run tests with ID 7, 4, 1, 2, and 5
>>> test_manager SVIN - Run test with ID 4
>>> test_manager DISC SCP CHIN - Run tests with ID 1, 6, and 3
>>> test_manager 24 vNw 314 ScP - Run tests with ID 2, 4, 7, 3, 1, and 6
>>> test_manager ^345 - Run all tests except those with ID 3, 4, and 5
>>> test_manager 100.68.125.170 5! - Run all tests on specified host except test 5
>>> test_manager host:node-example 345 - Run tests with ID 3, 4, 5 on specified host

:Copyright: (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
:License: Apache 2.0, see LICENSE for more details.

Created on June 20, 2017

'''
__title__ = 'test_manager'
__author__ = 'Akash Kwatra'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2017 DELL Inc.'

import sys
import unittest
import re
import logging
import logging.config

from discoveryTest import DiscoveryMicroserviceTest as disc
from chassisInventoryTest import ChassisInventoryMicroserviceTest as chin
from serverInventoryTest import ServerInventoryMicroserviceTest as svin
from powerThermalTest import PowerThermalMicroserviceTest as pwth
from scpTest import SCPMicroserviceTest as scp
from virtualIdentityTest import VirtualIdentityTest as vid
from virtualNetworkTest import VirtualNetworkTest as vnw
from firmwareUpdateTest import FirmwareUpdateTest as fwup
from dummy_tests import DummyTest as dummy

def configure_logger_from_yaml(path):
    """Attempts to configure root logger from given YAML file"""
    import yaml
    try:
        with open(path, 'r') as stream:
            config = yaml.load(stream)
            logging.config.dictConfig(config)
    except (FileNotFoundError, yaml.YAMLError) as exc:
        print("Could not load logger configuraton from YAML file :: {}".format(exc))



configure_logger_from_yaml('../logs/logger_config.yml')
LOG = logging.getLogger(__name__)

# ------------ ARGUMENT CONFIGURATION PROFILE ------------
##########################################################

# Default Host
HOST = "localhost"

# Microservice ID
M_ID = {

    '1' : disc,
    '2' : chin,
    '3' : svin,
    '4' : pwth,
    '5' : scp,
    '6' : vid,
    '7' : vnw,
    '8' : fwup,
    'D' : dummy


}

# Microservice ID Reversed
M_ID_R = {m_id: mservice for mservice, m_id in M_ID.items()}

# Microservice Alias
ALIAS = {

    'DISC' : M_ID_R[disc],
    'CHIN' : M_ID_R[chin],
    'SVIN' : M_ID_R[svin],
    'PWTH' : M_ID_R[pwth],
    'SCP' : M_ID_R[scp],
    'VID' : M_ID_R[vid],
    'VNW' : M_ID_R[vnw],
    'FWUP' : M_ID_R[fwup],
    'DUMMY' : M_ID_R[dummy]

}

##########################################################

def _parse_arguments(arguments):
    """Parse data from arguments to determine which tests will be loaded"""
    test_keys = set() # Store all keys for tests to run
    remove_keys = set() # Store all keys for tests to skip
    test_arguments = [] # Arguments to be parsed into keys
    remove_arguments = [] # Arguments to be parsed into keys
    host = HOST
    if arguments:
        # Parse out special arguments
        for arg in arguments:
            # Check for host IP address
            if re.search("localhost|\\.", str(arg).lower()):
                host = str(arg).lower()
            # Check for named host
            elif re.search("host:", str(arg).lower()):
                host = re.sub("host:", "", str(arg).lower())
            # Check for skip modifiers
            elif re.search("[\\^\\!]", str(arg)):
                remove_arguments.append(re.sub("[\\^\\!]", "", str(arg)))
            else:
                test_arguments.append(arg)
    # Default run all tests
    if not test_arguments:
        test_arguments = {val for val in ALIAS.values()}

    def _add_arguments_to_set(set_arguments, target_set):
        """ Take in arguments with special parameters removed and add to target set """
        def _add_key_from_m_id(m_id_string):
            for m_id in str(m_id_string):
                if m_id in M_ID:
                    target_set.add(m_id)
                else:
                    raise ValueError('Invalid Microservice ID - {}'.format(m_id))

        def _add_key_from_alias(alias):
            alias = alias.upper()
            if alias in ALIAS:
                target_set.add(ALIAS[alias])
            else:
                raise ValueError('Invalid Microservice Alias - {}'.format(alias))

        for arg in set_arguments:
            if str(arg).upper() in ALIAS:
                _add_key_from_alias(arg)
            elif str(arg).isalnum():
                _add_key_from_m_id(arg)
            else:
                raise ValueError('Invalid Argument - {}'.format(str(arg)))

    _add_arguments_to_set(remove_arguments, remove_keys)
    _add_arguments_to_set(test_arguments, test_keys)
    return host, (test_keys - remove_keys)

def _load_tests(test_keys):
    """Load tests into suite for each of the test keys passed in"""
    test_suite = []
    for key in test_keys:
        test_suite.append(unittest.TestLoader().loadTestsFromTestCase(M_ID[key]))
    return unittest.TestSuite(test_suite)

def run_tests(*args):
    """Run specified tests using arguments"""
    arguments = [arg for arg in args]
    LOG.info("Input: %s", arguments)
    host, keys = _parse_arguments(arguments)
    LOG.info("Host: %s", host)
    LOG.info("Test Keys: %s", keys)
    test_suite = _load_tests(keys)
    LOG.debug("Loaded Tests: %s", test_suite)
    unittest.TextTestRunner(verbosity=2).run(test_suite)

def _parse_keys_tester():
    """Test cases to make sure correct keys are parsed from given arguments"""
    test_cases = [[], [123], ['SCP'], ['chin', 2, 'DIsc'], [13, 'vnw', 455],
                  ['^5'], ['host:node-wright'], ['!chin'], ['192.168.0.1'],
                  ['localhost', 32, 'SCP', '^3', '!2', '100.0.0.255'],
                  ['host:node-example', '5!'], ['^1237']]
    print("\nBegin Testing\n\nID : ALIAS\n")
    for alias in ALIAS:
        print("{} : {}".format(ALIAS[alias], alias))
    print("\n")
    for index, case in enumerate(test_cases):
        LOG.info("Running test %s", (index + 1))
        print("\n--Test {}--\n Args:{}".format(index + 1, case))
        host, keys = _parse_arguments(case)
        print("Host: {}".format(host))
        print("Parsed Keys: {}\n".format(keys))

if __name__ == '__main__':
    # _parse_keys_tester()
    run_tests(*sys.argv[1:])
